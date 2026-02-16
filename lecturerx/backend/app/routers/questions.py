import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.lecture import Lecture
from app.models.practice_question import PracticeQuestion, QuestionAttempt
from app.models.user import User
from app.schemas.question import PracticeQuestionRead, QuestionAttemptCreate, QuestionAttemptRead

router = APIRouter(tags=["questions"])


@router.get("/api/lectures/{lecture_id}/questions", response_model=list[PracticeQuestionRead])
async def get_questions(
    lecture_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> list[PracticeQuestion]:
    lecture_result = await db.execute(select(Lecture.id).where(Lecture.id == lecture_id, Lecture.user_id == user.id))
    if lecture_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")

    result = await db.execute(select(PracticeQuestion).where(PracticeQuestion.lecture_id == lecture_id))
    return list(result.scalars().all())


@router.post("/api/questions/{question_id}/attempt", response_model=QuestionAttemptRead, status_code=status.HTTP_201_CREATED)
async def submit_attempt(
    question_id: uuid.UUID,
    payload: QuestionAttemptCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> QuestionAttempt:
    result = await db.execute(
        select(PracticeQuestion)
        .join(Lecture, Lecture.id == PracticeQuestion.lecture_id)
        .where(PracticeQuestion.id == question_id, Lecture.user_id == user.id)
    )
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    attempt = QuestionAttempt(
        user_id=user.id,
        question_id=question.id,
        selected_answer=payload.selected_answer,
        is_correct=payload.selected_answer.upper() == question.correct_answer.upper(),
        time_spent_seconds=payload.time_spent_seconds,
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt
