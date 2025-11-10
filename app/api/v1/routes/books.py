from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookRead
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[BookRead])
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.deleted_at.is_(None)))
    books = result.scalars().all()
    return books


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.book_id == book_id, Book.deleted_at.is_(None)))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(**payload.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


@router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, payload: BookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.book_id == book_id, Book.deleted_at.is_(None)))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(book, key, value)

    book.updated_at = datetime.utcnow()
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.book_id == book_id, Book.deleted_at.is_(None)))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book.deleted_at = datetime.utcnow()
    db.add(book)
    await db.commit()
    return None
