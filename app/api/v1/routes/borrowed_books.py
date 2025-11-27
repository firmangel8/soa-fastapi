from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.core.database import get_db
from app.models.borrowed_book import BorrowedBook
from app.schemas.borrowed_book import BorrowedBookCreate, BorrowedBookUpdate, BorrowedBookRead

import dotenv
from app.helper.payload import delivery_report
import msgpack
from confluent_kafka import Producer

from app.core.config import settings

TOPIC_NAME = settings.TOPIC_NAME

kafka_config = {
    'bootstrap.servers': settings.KAFKA_NETWORK,
}
producer = Producer(kafka_config)

router = APIRouter()

@router.get("/", response_model=list[BorrowedBookRead])
async def list_borrowed_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BorrowedBook).where(BorrowedBook.deleted_at.is_(None)))
    borrowed_books = result.scalars().all()
    return borrowed_books


@router.get("/{borrow_id}", response_model=BorrowedBookRead)
async def get_borrowed_book(borrow_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BorrowedBook).where(BorrowedBook.borrow_id == borrow_id, BorrowedBook.deleted_at.is_(None))
    )
    borrowed_book = result.scalar_one_or_none()
    if not borrowed_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    return borrowed_book


@router.post("/", response_model=BorrowedBookRead, status_code=status.HTTP_201_CREATED)
async def create_borrowed_book(payload: BorrowedBookCreate, db: AsyncSession = Depends(get_db)):
    serialized_payload = payload.json()
    new_borrowed_book = BorrowedBook(**payload.dict())
    db.add(new_borrowed_book)
    await db.commit()
    await db.refresh(new_borrowed_book)
    # send data to KAFKA_NETWORK
    data = {
        "topic": settings.TOPIC_NAME,
        "message": serialized_payload,
        "sender": "msg-pack-agent"
    }
    encoded_data = msgpack.packb(data, use_bin_type=True)
    producer.produce(TOPIC_NAME, encoded_data, on_delivery=delivery_report)
    producer.poll(0)
    producer.flush()
    return new_borrowed_book


@router.put("/{borrow_id}", response_model=BorrowedBookRead)
async def update_borrowed_book(borrow_id: int, payload: BorrowedBookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BorrowedBook).where(BorrowedBook.borrow_id == borrow_id, BorrowedBook.deleted_at.is_(None))
    )
    borrowed_book = result.scalar_one_or_none()
    if not borrowed_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(borrowed_book, key, value)

    borrowed_book.updated_at = datetime.utcnow()
    db.add(borrowed_book)
    await db.commit()
    await db.refresh(borrowed_book)
    return borrowed_book


@router.delete("/{borrow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_borrowed_book(borrow_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BorrowedBook).where(BorrowedBook.borrow_id == borrow_id, BorrowedBook.deleted_at.is_(None))
    )
    borrowed_book = result.scalar_one_or_none()
    if not borrowed_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")

    borrowed_book.deleted_at = datetime.utcnow()
    db.add(borrowed_book)
    await db.commit()
    return None
