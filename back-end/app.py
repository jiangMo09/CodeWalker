from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from utils.mysql import get_db, execute_query
from routers import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.codewalker.cc"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


class Question(BaseModel):
    id: int
    pretty_name: str
    kebab_case_name: str


class QuestionsList(BaseModel):
    questions: List[Question]


class Response(BaseModel):
    data: QuestionsList


@app.get("/questions_list", response_model=Response, tags=["home"])
async def get_questions_list(db=Depends(get_db)):
    try:
        query = "SELECT id, pretty_name, kebab_case_name FROM questions"
        result = execute_query(db, query, fetch_method="fetchall")
        questions_list = [
            Question(
                id=row["id"],
                pretty_name=row["pretty_name"],
                kebab_case_name=row["kebab_case_name"],
            )
            for row in result
        ]
        return Response(data=QuestionsList(questions=questions_list))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/ranking", tags=["home"])
async def get_ranking():
    return {"message": "/ranking"}
