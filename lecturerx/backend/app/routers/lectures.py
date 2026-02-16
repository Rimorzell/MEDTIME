import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.lecture import Lecture
from app.models.user import User
from app.schemas.lecture import LectureCreate, LectureRead

router = APIRouter(prefix="/api/lectures", tags=["lectures"])


@router.post("", response_model=LectureRead, status_code=status.HTTP_201_CREATED)
async def create_lecture(payload: LectureCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> Lecture:
    lecture = Lecture(
        id=uuid.uuid4(),
        user_id=user.id,
        title=payload.title,
        file_url=payload.file_url,
        file_type=payload.file_type,
        file_size_bytes=payload.file_size_bytes,
    )
    db.add(lecture)
    await db.commit()
    await db.refresh(lecture)
    return lecture


@router.get("", response_model=list[LectureRead])
async def list_lectures(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> list[Lecture]:
    result = await db.execute(select(Lecture).where(Lecture.user_id == user.id).order_by(Lecture.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{lecture_id}", response_model=LectureRead)
async def get_lecture(lecture_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> Lecture:
    result = await db.execute(select(Lecture).where(Lecture.id == lecture_id, Lecture.user_id == user.id))
    lecture = result.scalar_one_or_none()
    if not lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")
    return lecture


@router.delete("/{lecture_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_lecture(lecture_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> Response:
    result = await db.execute(select(Lecture).where(Lecture.id == lecture_id, Lecture.user_id == user.id))
    lecture = result.scalar_one_or_none()
    if not lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")

    await db.execute(delete(Lecture).where(Lecture.id == lecture_id))
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
