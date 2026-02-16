import uuid

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    x_clerk_user_id: str | None = Header(default=None),
    x_user_email: str | None = Header(default=None),
) -> User:
    if not x_clerk_user_id or not x_user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth headers")

    result = await db.execute(select(User).where(User.clerk_id == x_clerk_user_id))
    user = result.scalar_one_or_none()
    if user:
        return user

    user = User(id=uuid.uuid4(), clerk_id=x_clerk_user_id, email=x_user_email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
