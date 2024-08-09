from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
import json

from utils.mysql import get_db, execute_query

router = APIRouter()


class QuestionDataInput(BaseModel):
    id: str
    title: str
    example_testcase_List: List[str]
    meta_data: str


class DataInputResponse(BaseModel):
    data: QuestionDataInput


@router.get("/question_data_input", response_model=DataInputResponse)
async def get_question_data_input(
    name: str = Query(..., description="The kebab case name of the question"),
    db=Depends(get_db),
):
    try:
        query = """
        SELECT id, pretty_name, 
               (SELECT meta_data FROM questions_test_cases WHERE question_id = questions.id LIMIT 1) as meta_data
        FROM questions 
        WHERE kebab_case_name = %s
        """
        result = execute_query(db, query, (name,), fetch_method="fetchone")

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        query_test_cases = """
        SELECT data_input_run, correct_answer_run 
        FROM questions_test_cases 
        WHERE question_id = %s 
        """
        test_cases = execute_query(
            db, query_test_cases, (result["id"],), fetch_method="fetchall"
        )

        example_testcase_List = [
            f"{case['data_input_run']}\n{case['correct_answer_run']}"
            for case in test_cases
        ]

        question_data = QuestionDataInput(
            id=str(result["id"]),
            title=result["pretty_name"],
            example_testcase_List=example_testcase_List,
            meta_data=result["meta_data"],
        )

        return DataInputResponse(data=question_data)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
