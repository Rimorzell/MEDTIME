import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LectureCreate(BaseModel):
    title: str
    file_url: str
    file_type: str
    file_size_bytes: int | None = None


class LectureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    file_url: str | None
    file_type: str
    file_size_bytes: int | None
    organ_system: str | None
    discipline: str | None
    processing_status: str
    processing_error: str | None
    slide_count: int | None
    concept_count: int
    flashcard_count: int
    question_count: int
    created_at: datetime
    updated_at: datetime
