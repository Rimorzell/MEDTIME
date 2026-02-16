import uuid
from datetime import datetime

from sqlalchemy import ARRAY, Boolean, CHAR, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import UUIDMixin


class PracticeQuestion(Base, UUIDMixin):
    __tablename__ = "practice_questions"
    __table_args__ = (Index("idx_questions_lecture_id", "lecture_id"),)

    lecture_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lectures.id", ondelete="CASCADE"), nullable=False)
    concept_ids: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=True)
    question_stem: Mapped[str] = mapped_column(Text, nullable=False)
    answer_choices: Mapped[list[dict[str, str]]] = mapped_column(JSONB, nullable=False)
    correct_answer: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    lecture = relationship("Lecture", back_populates="questions")
    attempts = relationship("QuestionAttempt", back_populates="question", cascade="all, delete-orphan")


class QuestionAttempt(Base, UUIDMixin):
    __tablename__ = "question_attempts"
    __table_args__ = (Index("idx_attempts_user_id", "user_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("practice_questions.id", ondelete="CASCADE"), nullable=False
    )
    selected_answer: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_spent_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="attempts")
    question = relationship("PracticeQuestion", back_populates="attempts")
