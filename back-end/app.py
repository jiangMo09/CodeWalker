from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from utils.mysql import get_db, execute_query
from utils.redis_client import get_redis_client, execute_redis_command
from helpers.leaderboard import get_total_leaderboard
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


class LeaderboardEntry(BaseModel):
    username: str
    score: float


class LeaderboardResponse(BaseModel):
    data: List[LeaderboardEntry]


@app.get("/ranking", response_model=LeaderboardResponse, tags=["home"])
async def get_ranking(db=Depends(get_db)):
    try:
        leaderboard = await get_total_leaderboard(limit=10)

        if not leaderboard:
            query = """
            SELECT u.username, SUM(s.score) as total_score
            FROM submissions s
            JOIN users u ON s.user_id = u.id
            GROUP BY s.user_id
            ORDER BY total_score DESC
            LIMIT 10
            """
            result = execute_query(db, query, fetch_method="fetchall")
            leaderboard = [
                {
                    "username": row["username"],
                    "score": round(float(row["total_score"]), 2),
                }
                for row in result
            ]

            redis = await get_redis_client()
            leaderboard_key = "{leaderboard}:total"
            pipeline = redis.pipeline()
            for entry in leaderboard:
                pipeline.zadd(leaderboard_key, {entry["username"]: entry["score"]})
            await execute_redis_command(pipeline.execute)

        formatted_leaderboard = [
            LeaderboardEntry(username=entry["username"], score=entry["score"])
            for entry in leaderboard
        ]

        return {"data": formatted_leaderboard}
    except Exception as e:
        print(f"Error in get_ranking: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
