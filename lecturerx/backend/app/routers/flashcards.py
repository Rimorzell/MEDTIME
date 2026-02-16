import io
import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.flashcard import Flashcard
from app.models.lecture import Lecture
from app.models.user import User
from app.schemas.flashcard import FlashcardRead, FlashcardUpdate

router = APIRouter(tags=["flashcards"])


@router.get("/api/lectures/{lecture_id}/flashcards", response_model=list[FlashcardRead])
async def get_flashcards(
    lecture_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> list[Flashcard]:
    lecture_result = await db.execute(select(Lecture.id).where(Lecture.id == lecture_id, Lecture.user_id == user.id))
    if lecture_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")

    result = await db.execute(select(Flashcard).where(Flashcard.lecture_id == lecture_id))
    return list(result.scalars().all())


@router.put("/api/flashcards/{flashcard_id}", response_model=FlashcardRead)
async def update_flashcard(
    flashcard_id: uuid.UUID,
    payload: FlashcardUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Flashcard:
    result = await db.execute(
        select(Flashcard)
        .join(Lecture, Lecture.id == Flashcard.lecture_id)
        .where(Flashcard.id == flashcard_id, Lecture.user_id == user.id)
    )
    flashcard = result.scalar_one_or_none()
    if not flashcard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found")

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(flashcard, key, value)

    flashcard.is_edited = True
    await db.commit()
    await db.refresh(flashcard)
    return flashcard


@router.post("/api/flashcards/{flashcard_id}/flag", response_model=FlashcardRead)
async def flag_flashcard(
    flashcard_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Flashcard:
    result = await db.execute(
        select(Flashcard)
        .join(Lecture, Lecture.id == Flashcard.lecture_id)
        .where(Flashcard.id == flashcard_id, Lecture.user_id == user.id)
    )
    flashcard = result.scalar_one_or_none()
    if not flashcard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found")

    flashcard.is_flagged_incorrect = True
    await db.commit()
    await db.refresh(flashcard)
    return flashcard


@router.get("/api/lectures/{lecture_id}/flashcards/export")
async def export_flashcards(
    lecture_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Response:
    result = await db.execute(select(Lecture).where(Lecture.id == lecture_id, Lecture.user_id == user.id))
    lecture = result.scalar_one_or_none()
    if not lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")

    # Placeholder APKG response for infrastructure setup.
    output = io.BytesIO(b"placeholder-apkg")
    headers = {"Content-Disposition": f'attachment; filename="{lecture.title}.apkg"'}
    return Response(content=output.getvalue(), media_type="application/octet-stream", headers=headers)
