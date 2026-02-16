import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuestionAttemptCreate(BaseModel):
    selected_answer: str
    time_spent_seconds: int | None = None


class PracticeQuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lecture_id: uuid.UUID
    concept_ids: list[uuid.UUID] | None
    question_stem: str
    answer_choices: list[dict[str, str]]
    correct_answer: str
    explanation: str
    difficulty: str
    created_at: datetime


class QuestionAttemptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    question_id: uuid.UUID
    selected_answer: str
    is_correct: bool
    time_spent_seconds: int | None
    attempted_at: datetime
