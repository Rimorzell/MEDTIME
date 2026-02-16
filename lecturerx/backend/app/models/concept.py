import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import UUIDMixin


class Concept(Base, UUIDMixin):
    __tablename__ = "concepts"
    __table_args__ = (Index("idx_concepts_lecture_id", "lecture_id"),)

    lecture_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lectures.id", ondelete="CASCADE"), nullable=False)
    concept_name: Mapped[str] = mapped_column(String(500), nullable=False)
    definition: Mapped[str | None] = mapped_column(Text, nullable=True)
    key_facts: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    discipline: Mapped[str | None] = mapped_column(String(100), nullable=True)
    organ_system: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_slide_numbers: Mapped[list[int] | None] = mapped_column(ARRAY(Integer), nullable=True)
    board_relevance: Mapped[str | None] = mapped_column(String(50), nullable=True)
    board_topic_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("board_topics.id", ondelete="SET NULL"), nullable=True
    )
    board_topic_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    mapping_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    first_aid_chapter: Mapped[int | None] = mapped_column(Integer, nullable=True)
    first_aid_section: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    lecture = relationship("Lecture", back_populates="concepts")
    board_topic = relationship("BoardTopic", back_populates="concepts")
    flashcards = relationship("Flashcard", back_populates="concept")
