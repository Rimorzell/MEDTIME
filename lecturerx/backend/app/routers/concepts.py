import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.concept import Concept
from app.models.lecture import Lecture
from app.models.user import User
from app.schemas.concept import ConceptRead

router = APIRouter(tags=["concepts"])


@router.get("/api/lectures/{lecture_id}/concepts", response_model=list[ConceptRead])
async def get_lecture_concepts(
    lecture_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> list[Concept]:
    lecture_result = await db.execute(select(Lecture.id).where(Lecture.id == lecture_id, Lecture.user_id == user.id))
    if lecture_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")

    result = await db.execute(select(Concept).where(Concept.lecture_id == lecture_id))
    return list(result.scalars().all())
