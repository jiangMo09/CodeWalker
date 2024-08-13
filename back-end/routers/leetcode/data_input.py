from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List
from utils.mysql import get_db, execute_query

router = APIRouter()


class QuestionDataInput(BaseModel):
    id: str
    example_testcase_list: List[str] = Field(..., alias="example_testcase_List")
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
        SELECT q.id, qtc.meta_data
        FROM questions q
        LEFT JOIN questions_test_cases qtc ON q.id = qtc.question_id
        WHERE q.kebab_case_name = %s
        LIMIT 1
        """
        result = execute_query(db, query, (name,), fetch_method="fetchone")

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        query_test_cases = """
        SELECT data_input_run
        FROM questions_test_cases 
        WHERE question_id = %s 
        """
        test_cases = execute_query(
            db, query_test_cases, (result["id"],), fetch_method="fetchall"
        )

        example_testcase_list = [case["data_input_run"] for case in test_cases]

        question_data = QuestionDataInput(
            id=str(result["id"]),
            example_testcase_List=example_testcase_list,
            meta_data=result["meta_data"] or "",
        )

        return DataInputResponse(data=question_data)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
