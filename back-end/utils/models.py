from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    id: int
    name: str
    description: str = None


class QuestionsList(BaseModel):
    questions: List[Question]


class Response(BaseModel):
    data: QuestionsList
