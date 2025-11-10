from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorRead
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[AuthorRead])
async def list_authors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.deleted_at.is_(None)))
    authors = result.scalars().all()
    return authors


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.author_id == author_id, Author.deleted_at.is_(None)))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
async def create_author(payload: AuthorCreate, db: AsyncSession = Depends(get_db)):
    new_author = Author(**payload.dict())
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author


@router.put("/{author_id}", response_model=AuthorRead)
async def update_author(author_id: int, payload: AuthorUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.author_id == author_id, Author.deleted_at.is_(None)))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(author, key, value)

    author.updated_at = datetime.utcnow()
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.author_id == author_id, Author.deleted_at.is_(None)))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    author.deleted_at = datetime.utcnow()
    db.add(author)
    await db.commit()
    return None
