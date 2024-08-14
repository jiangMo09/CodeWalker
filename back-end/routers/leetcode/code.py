import json
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Dict

from .docker_manager import run_container
from utils.mysql import get_db, execute_query

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


async def execute_code(data):
    language = data.get("lang", "")

    language_to_image = {
        "javascript": "js-docker",
        "python": "python-docker",
        "java": "java-docker",
        "cpp": "cpp-docker",
    }

    if language not in language_to_image:
        raise ValueError(f"不支援的語言: {language}")

    image_name = language_to_image[language]
    result = await run_container(image_name, data)
    return result


@router.post("/question_code")
async def post_question_code(typed_code: CodeTyped, db=Depends(get_db)):
    try:
        question_query = (
            "SELECT id, camel_case_name, parameters_count FROM questions WHERE id = %s"
        )
        question_result = execute_query(
            db, question_query, (typed_code.question_id,), fetch_method="fetchone"
        )
        if not question_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        submit_status = "submit" if typed_code.submit else "run"
        test_cases_query = f"SELECT data_input_{submit_status}, correct_answer_{submit_status} FROM questions_test_cases WHERE question_id = %s"
        test_cases_result = execute_query(
            db, test_cases_query, (typed_code.question_id,), fetch_method="fetchone"
        )
        print("test_cases_result", test_cases_result)


        if not test_cases_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test cases not found"
            )

        docker_input = {
            "data_input": test_cases_result[f"data_input_{submit_status}"],
            "correct_answer": test_cases_result[f"correct_answer_{submit_status}"],
            "lang": typed_code.lang,
            "question_id": str(typed_code.question_id),
            "function_name": question_result["camel_case_name"],
            "typed_code": typed_code.typed_code,
            "parameters_count": question_result["parameters_count"],
        }
        result = await execute_code(docker_input)
        return {"data": result}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
