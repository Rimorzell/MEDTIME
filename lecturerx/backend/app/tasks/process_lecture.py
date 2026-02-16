import logging
import uuid

from sqlalchemy import update

from app.database import AsyncSessionLocal
from app.models.lecture import Lecture
from app.tasks import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="process_lecture")
def process_lecture(lecture_id: str) -> None:
    logger.info("Processing lecture %s", lecture_id)

    async def _update_status() -> None:
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(Lecture)
                .where(Lecture.id == uuid.UUID(lecture_id))
                .values(processing_status="parsing")
            )
            await session.commit()

    import asyncio

    asyncio.run(_update_status())
