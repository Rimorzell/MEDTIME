import uuid

from sqlalchemy import BigInteger, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDMixin


class Lecture(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lectures"
    __table_args__ = (Index("idx_lectures_user_id", "user_id"), Index("idx_lectures_status", "processing_status"))

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    organ_system: Mapped[str | None] = mapped_column(String(100), nullable=True)
    discipline: Mapped[str | None] = mapped_column(String(100), nullable=True)
    processing_status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    slide_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    concept_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    flashcard_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    question_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="lectures")
    concepts = relationship("Concept", back_populates="lecture", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="lecture", cascade="all, delete-orphan")
    questions = relationship("PracticeQuestion", back_populates="lecture", cascade="all, delete-orphan")
