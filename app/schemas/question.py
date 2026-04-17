from pydantic import BaseModel
from typing import List, Optional

class Option(BaseModel):
    id: str
    text: str
    score: int

class Question(BaseModel):
    id: str
    category: str
    question: str
    options: List[Option]
    feedback: dict

class QuestionAnswer(BaseModel):
    question_id: str
    option_id: str

class QuestionSubmit(BaseModel):
    answers: List[QuestionAnswer]

class QuestionResult(BaseModel):
    total_score: int
    level: str
    message: str
    feedback: List[dict]
