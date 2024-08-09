from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel

from utils.mysql import get_db_connection, execute_query

router = APIRouter()


class QuestionDescription(BaseModel):
    id: int
    pretty_name: str
    description: str


class QuestionResponse(BaseModel):
    data: QuestionDescription


@router.get("/question_description", response_model=QuestionResponse)
async def get_question_description(
    name: str = Query(..., description="The kebab case name of the question")
):
    connection = None
    try:
        connection = get_db_connection()
        query = "SELECT id, pretty_name, description FROM questions WHERE kebab_case_name = %s"
        result = execute_query(connection, query, (name,), fetch_method="fetchone")

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        question_data = QuestionDescription(**result)
        return QuestionResponse(data=question_data)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if connection:
            connection.close()
