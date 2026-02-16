import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConceptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lecture_id: uuid.UUID
    concept_name: str
    definition: str | None
    key_facts: list[str] | None
    discipline: str | None
    organ_system: str | None
    source_slide_numbers: list[int] | None
    board_relevance: str | None
    board_topic_id: uuid.UUID | None
    board_topic_name: str | None
    mapping_confidence: float | None
    first_aid_chapter: int | None
    first_aid_section: str | None
    created_at: datetime
