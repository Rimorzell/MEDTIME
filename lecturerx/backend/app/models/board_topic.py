import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, DateTime, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import UUIDMixin


class BoardTopic(Base, UUIDMixin):
    __tablename__ = "board_topics"
    __table_args__ = (
        Index(
            "idx_board_topics_embedding",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
        Index("idx_board_topics_organ_system", "organ_system"),
    )

    topic_name: Mapped[str] = mapped_column(String(500), nullable=False)
    organ_system: Mapped[str] = mapped_column(String(100), nullable=False)
    discipline: Mapped[str] = mapped_column(String(100), nullable=False)
    subdiscipline: Mapped[str | None] = mapped_column(String(100), nullable=True)
    yield_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    first_aid_chapter: Mapped[int | None] = mapped_column(Integer, nullable=True)
    first_aid_section: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_aid_page: Mapped[int | None] = mapped_column(Integer, nullable=True)
    keywords: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    related_topic_ids: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    concepts = relationship("Concept", back_populates="board_topic")
