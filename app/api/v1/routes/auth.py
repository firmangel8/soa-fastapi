from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.core.database import get_db
from app.core.auth import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)

from app.models.user import User
from app.schemas.user import UserCreate, UserRead

from app.core.security import verify_password, hash_password

from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    query = select(User).where(
        User.username == payload.username,
        User.deleted_at.is_(None)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # verify password
    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # create tokens
    access_token = create_access_token({"sub": user.id_users, "name": user.username})
    refresh_token = create_refresh_token({"sub": user.id_users, "name": user.username})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.post("/register", response_model=UserRead)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # check if username exists
    existing = await db.execute(select(User).where(User.username == payload.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=payload.username,
        password=hash_password(payload.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
