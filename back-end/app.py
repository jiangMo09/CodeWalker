from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from utils.mysql import get_db_connection, execute_query


app = FastAPI()


@app.get("/api/questions_list")
async def get_questions_list():
    connection = None
    try:
        connection = get_db_connection()
        query = "SELECT id, pretty_name FROM questions"
        result = execute_query(connection, query, None, fetch_method="fetchall")

        questions_list = [
            {"id": row["id"], "name": row["pretty_name"]} for row in result
        ]

        response_data = {"data": {"questions": questions_list}}

        return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)}
        )
    finally:
        if connection:
            connection.close()


@app.get("/api/ranking")
async def get_ranking():
    return {"message": "/api/ranking"}
