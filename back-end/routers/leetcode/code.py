from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel


from utils.mysql import get_db, execute_query
from utils.models import Response

router = APIRouter()


class CodeSnippet(BaseModel):
    lang: str
    langSlug: str
    code: str


class Language(BaseModel):
    id: int
    name: str
    pretty_name: str


@router.get("/question_code", response_model=Response)
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

        return Response(
            data={"code_snippets": [snippet.dict() for snippet in code_snippets]}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/language_list", response_model=Response)
async def get_language_list(db=Depends(get_db)):
    try:
        query = "SELECT id, name, pretty_name FROM languages"
        result = execute_query(db, query, fetch_method="fetchall")

        language_list = [
            Language(id=row["id"], name=row["name"], pretty_name=row["pretty_name"])
            for row in result
        ]

        return Response(data={"language_list": [lang.dict() for lang in language_list]})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
