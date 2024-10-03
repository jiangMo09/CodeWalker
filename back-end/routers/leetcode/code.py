from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
    Request,
    BackgroundTasks,
    Header,
)
from pydantic import BaseModel
from typing import List, Dict
import jwt
import uuid
import json
import boto3

from .docker_manager import run_container
from utils.mysql import get_db, execute_query, get_db_connection
from utils.load_env import JWT_SECRET_KEY, ENVIRONMENT, SQS_URL, AWS_BUCKET_REGION
from utils.redis_client import get_redis_client, execute_redis_command
from helpers.leaderboard import update_leaderboard
from helpers.score import calculate_score


router = APIRouter()


class CodeSnippet(BaseModel):
    lang: str
    langSlug: str
    code: str


class Languages(BaseModel):
    id: int
    name: str
    pretty_name: str


class CodeResponse(BaseModel):
    data: Dict[str, List[CodeSnippet]]


class LanguagesResponse(BaseModel):
    data: List[Languages]


class CodeTyped(BaseModel):
    lang: str
    question_id: int
    submit: bool
    typed_code: str


@router.get("/question_code", response_model=CodeResponse)
async def get_question_code(
    name: str = Query(..., description="The kebab case name of the question"),
    db=Depends(get_db),
):
    try:
        question_query = "SELECT id FROM questions WHERE kebab_case_name = %s"
        question_result = execute_query(
            db, question_query, (name,), fetch_method="fetchone"
        )
        if not question_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        question_id = question_result["id"]

        snippets_query = """
        SELECT l.pretty_name as lang, l.name as langSlug, qp.prototypes as code
        FROM questions_prototypes qp
        JOIN languages l ON qp.language_id = l.id
        WHERE qp.question_id = %s
        """
        snippets_result = execute_query(
            db, snippets_query, (question_id,), fetch_method="fetchall"
        )

        code_snippets = [
            CodeSnippet(lang=row["lang"], langSlug=row["langSlug"], code=row["code"])
            for row in snippets_result
        ]

        return CodeResponse(
            data={"code_snippets": [snippet.dict() for snippet in code_snippets]}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/languages_list", response_model=LanguagesResponse)
async def get_language_list(db=Depends(get_db)):
    try:
        query = "SELECT id, name, pretty_name FROM languages"
        result = execute_query(db, query, fetch_method="fetchall")

        language_list = [
            Languages(id=row["id"], name=row["name"], pretty_name=row["pretty_name"])
            for row in result
        ]

        return LanguagesResponse(data=language_list)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


EXPIRATION_TIME = 300


async def execute_code(image_name, data):
    return await run_container(image_name, data)


async def store_result_in_redis(redis_key, result):
    redis_client = await get_redis_client()
    await execute_redis_command(
        redis_client.set, redis_key, json.dumps(result), ex=EXPIRATION_TIME
    )


async def update_submission_if_needed(conn, user_id, typed_code, result):
    if not (
        typed_code.submit and result["container_run_success"] and result["all_passed"]
    ):
        return

    update_submission_data(conn, user_id, typed_code, result)


async def update_leaderboard_if_needed(typed_code, result, username):
    if not (
        typed_code.submit and result["container_run_success"] and result["all_passed"]
    ):
        return

    percentile = await update_leaderboard(
        typed_code.question_id,
        float(result["total_run_time"].split()[0]),
        username,
        calculate_score(result),
    )
    if percentile is not None:
        result["percentile"] = percentile


async def execute_code_background(data, redis_key, user_id, username, typed_code):
    redis_client = await get_redis_client()

    await execute_redis_command(
        redis_client.set,
        redis_key,
        json.dumps({"status": "running"}),
        ex=EXPIRATION_TIME,
    )

    language = data.get("lang", "")
    language_to_image = {
        "javascript": "js-docker",
        "python3": "python-docker",
        "java": "java-docker",
        "cpp": "cpp-docker",
    }

    if language not in language_to_image:
        raise ValueError(f"不支援的語言: {language}")

    image_name = language_to_image[language]
    result = await execute_code(image_name, data)

    with get_db_connection() as conn:
        await update_submission_if_needed(conn, user_id, typed_code, result)

    await update_leaderboard_if_needed(typed_code, result, username)
    await store_result_in_redis(redis_key, result)


sqs = boto3.client("sqs", region_name=AWS_BUCKET_REGION)


@router.post("/question_code")
async def post_question_code(
    request: Request, typed_code: CodeTyped, background_tasks: BackgroundTasks
):
    auth_token = request.headers.get("authToken")

    payload = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms=["HS256"])
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please Login",
        )
    user_id = payload["id"]
    username = payload["username"]

    try:
        with get_db_connection() as conn:
            question_result, test_cases_result = get_question_and_test_cases(
                conn, typed_code
            )

        docker_input = prepare_docker_input(
            question_result, test_cases_result, typed_code
        )

        task_id = str(uuid.uuid4())[:4]

        submit_status = "submit" if typed_code.submit else "run"
        redis_key = f"{user_id}_{typed_code.question_id}_{submit_status}_{task_id}"

        if ENVIRONMENT == "production":
            message_body = json.dumps(
                {
                    "docker_input": docker_input,
                    "redis_key": redis_key,
                    "user_id": user_id,
                    "username": username,
                    "typed_code": typed_code.dict(),
                }
            )

            sqs.send_message(QueueUrl=SQS_URL, MessageBody=message_body)

            print(f"Task sent to SQS: {redis_key}")
        else:
            background_tasks.add_task(
                execute_code_background,
                docker_input,
                redis_key,
                user_id,
                username,
                typed_code,
            )
            print(f"Task executed locally: {redis_key}")

        return {"data": {"question_result_id": redis_key}}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def get_question_and_test_cases(conn, typed_code):
    question_query = (
        "SELECT id, function_name, parameters_count FROM questions WHERE id = %s"
    )
    question_result = execute_query(
        conn, question_query, (typed_code.question_id,), fetch_method="fetchone"
    )
    if not question_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    submit_status = "submit" if typed_code.submit else "run"
    test_cases_query = f"SELECT data_input_{submit_status}, correct_answer_{submit_status} FROM questions_test_cases WHERE question_id = %s"
    test_cases_result = execute_query(
        conn, test_cases_query, (typed_code.question_id,), fetch_method="fetchone"
    )

    if not test_cases_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test cases not found"
        )

    return question_result, test_cases_result


def prepare_docker_input(question_result, test_cases_result, typed_code):
    submit_status = "submit" if typed_code.submit else "run"
    return {
        "data_input": test_cases_result[f"data_input_{submit_status}"],
        "correct_answer": test_cases_result[f"correct_answer_{submit_status}"],
        "lang": typed_code.lang,
        "question_id": str(typed_code.question_id),
        "function_name": question_result["function_name"],
        "typed_code": typed_code.typed_code,
        "parameters_count": question_result["parameters_count"],
    }


def update_submission_data(conn, user_id, typed_code, result):
    check_query = """
    SELECT id FROM submissions 
    WHERE user_id = %s AND question_id = %s
    """
    existing_submission = execute_query(
        conn,
        check_query,
        (user_id, typed_code.question_id),
        fetch_method="fetchone",
    )

    lang_query = "SELECT id FROM languages WHERE name = %s"
    lang_result = execute_query(
        conn, lang_query, (typed_code.lang,), fetch_method="fetchone"
    )
    language_id = lang_result["id"] if lang_result else None

    memory = float(result["total_run_memory"].split()[0])
    execution_time = float(result["total_run_time"].split()[0])
    score = calculate_score(result)

    if existing_submission:
        update_query = """
        UPDATE submissions 
        SET language_id = %s, memory = %s, execution_time = %s, score = %s
        WHERE id = %s
        """
        execute_query(
            conn,
            update_query,
            (
                language_id,
                memory,
                execution_time,
                score,
                existing_submission["id"],
            ),
        )
    else:
        insert_query = """
        INSERT INTO submissions 
        (user_id, question_id, language_id, memory, execution_time, score)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(
            conn,
            insert_query,
            (
                user_id,
                typed_code.question_id,
                language_id,
                memory,
                execution_time,
                score,
            ),
        )


@router.get("/execution_result/{redis_key}")
async def get_result(redis_key: str, authToken: str = Header(None)):
    if not authToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing",
        )

    try:
        payload = jwt.decode(authToken, JWT_SECRET_KEY, algorithms=["HS256"])
        auth_user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    redis_key_parts = redis_key.split("_")
    if len(redis_key_parts) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid redis key format"
        )

    redis_user_id = redis_key_parts[0]

    if str(auth_user_id) != redis_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
        )

    redis_client = await get_redis_client()
    result = await execute_redis_command(redis_client.get, redis_key)

    if result is None:
        raise HTTPException(status_code=404, detail="Result not found or expired")

    result_data = json.loads(result)

    if result_data.get("status") == "running":
        return {"data": {"status": "running", "message": "Code is still executing"}}

    return {"data": result_data}
