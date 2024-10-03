import sys
import json
import asyncio
from typing import NamedTuple
from helpers.leaderboard import update_leaderboard
from helpers.score import calculate_score
from utils.mysql import execute_query, get_db_connection
from utils.redis_client import get_redis_client, execute_redis_command
from docker_manager import run_container


class TypedCode(NamedTuple):
    lang: str
    question_id: int
    submit: bool
    typed_code: str


async def execute_code(image_name, data):
    return await run_container(image_name, data)


async def store_result_in_redis(redis_key, result):
    redis_client = await get_redis_client()
    await execute_redis_command(redis_client.set, redis_key, json.dumps(result), ex=300)


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
    async with await get_redis_client() as redis_client:
        try:
            await execute_redis_command(
                redis_client.set,
                redis_key,
                json.dumps({"status": "running"}),
                ex=300,
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
        except Exception as e:
            print(f"執行過程中發生錯誤: {str(e)}")
            await execute_redis_command(
                redis_client.set,
                redis_key,
                json.dumps({"status": "error", "message": str(e)}),
                ex=300,
            )


async def main():
    if len(sys.argv) < 2:
        print("Usage: python worker.py '<json_string>'")
        return

    input_data = json.loads(sys.argv[1])

    docker_input = input_data["docker_input"]
    redis_key = input_data["redis_key"]
    user_id = input_data["user_id"]
    username = input_data["username"]
    typed_code = TypedCode(**input_data["typed_code"])

    await execute_code_background(
        docker_input, redis_key, user_id, username, typed_code
    )


if __name__ == "__main__":
    asyncio.run(main())
