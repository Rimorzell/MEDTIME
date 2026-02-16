from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    clerk_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    medical_school: Mapped[str | None] = mapped_column(String(255), nullable=True)
    year_in_school: Mapped[int | None] = mapped_column(Integer, nullable=True)
    subscription_tier: Mapped[str] = mapped_column(String(50), default="free", nullable=False)
    lectures_processed_this_month: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    lectures = relationship("Lecture", back_populates="user", cascade="all, delete-orphan")
    attempts = relationship("QuestionAttempt", back_populates="user", cascade="all, delete-orphan")
