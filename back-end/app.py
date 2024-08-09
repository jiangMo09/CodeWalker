from fastapi import FastAPI, Depends, HTTPException, status
from utils.mysql import get_db, execute_query
from utils.models import Question, Response
from routers import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/api/questions_list", response_model=Response)
async def get_questions_list(db=Depends(get_db)):
    try:
        query = "SELECT id, pretty_name FROM questions"
        result = execute_query(db, query, fetch_method="fetchall")
        questions_list = [
            Question(id=row["id"], name=row["pretty_name"]) for row in result
        ]
        return Response(data={"questions": questions_list})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/api/ranking")
async def get_ranking():
    return {"message": "/api/ranking"}
