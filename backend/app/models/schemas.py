from pydantic import BaseModel
from typing import List, Optional


class Answer(BaseModel):
    question_id: str
    answer: str


class DiagnosticSubmission(BaseModel):
    student_id: str
    answers: List[Answer]


class QuizAnswer(BaseModel):
    question_id: str
    answer: str


class QuizSubmission(BaseModel):
    student_id: str
    concept_id: str
    answers: List[QuizAnswer]


class TutorRequest(BaseModel):
    student_id: str
    concept_id: str
    message: str
    language: Optional[str] = "English"


class AttemptData(BaseModel):
    attempt_id: str
    student_id: str
    question_id: str
    concept_id: str
    correct: bool
    selected_answer: str
    response_time_seconds: float
    attempt_number: int
    hint_used: bool
    confidence: float
    misconception_id: Optional[str] = None