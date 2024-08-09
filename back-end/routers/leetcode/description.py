from fastapi import APIRouter, Depends, HTTPException, status, Query
from utils.mysql import get_db, execute_query
from utils.models import Response, Question

router = APIRouter()


@router.get("/question_description", response_model=Response)
async def get_question_description(
    name: str = Query(..., description="The kebab case name of the question"),
    db=Depends(get_db),
):
    try:
        query = "SELECT id, pretty_name, description FROM questions WHERE kebab_case_name = %s"
        result = execute_query(db, query, (name,), fetch_method="fetchone")
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        question_data = Question(
            id=result["id"],
            name=result["pretty_name"],
            description=result["description"],
        )
        return Response(data={"questions": [question_data]})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
