import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FlashcardUpdate(BaseModel):
    front_text: str | None = None
    back_text: str | None = None
    tags: list[str] | None = None


class FlashcardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lecture_id: uuid.UUID
    concept_id: uuid.UUID | None
    front_text: str
    back_text: str
    card_type: str
    tags: list[str] | None
    board_topic: str | None
    source_slide_number: int | None
    is_edited: bool
    is_flagged_incorrect: bool
    created_at: datetime
