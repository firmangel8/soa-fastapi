from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.core.database import get_db
from app.models.borrower import Borrower
from app.schemas.borrower import BorrowerCreate, BorrowerUpdate, BorrowerRead

router = APIRouter()

@router.get("/", response_model=list[BorrowerRead])
async def list_borrowers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Borrower).where(Borrower.deleted_at.is_(None)))
    borrowers = result.scalars().all()
    return borrowers


@router.get("/{borrower_id}", response_model=BorrowerRead)
async def get_borrower(borrower_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Borrower).where(Borrower.borrower_id == borrower_id, Borrower.deleted_at.is_(None))
    )
    borrower = result.scalar_one_or_none()
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrower not found")
    return borrower


@router.post("/", response_model=BorrowerRead, status_code=status.HTTP_201_CREATED)
async def create_borrower(payload: BorrowerCreate, db: AsyncSession = Depends(get_db)):
    new_borrower = Borrower(**payload.dict())
    db.add(new_borrower)
    await db.commit()
    await db.refresh(new_borrower)
    return new_borrower


@router.put("/{borrower_id}", response_model=BorrowerRead)
async def update_borrower(borrower_id: int, payload: BorrowerUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Borrower).where(Borrower.borrower_id == borrower_id, Borrower.deleted_at.is_(None))
    )
    borrower = result.scalar_one_or_none()
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrower not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(borrower, key, value)

    borrower.updated_at = datetime.utcnow()
    db.add(borrower)
    await db.commit()
    await db.refresh(borrower)
    return borrower


@router.delete("/{borrower_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_borrower(borrower_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Borrower).where(Borrower.borrower_id == borrower_id, Borrower.deleted_at.is_(None))
    )
    borrower = result.scalar_one_or_none()
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrower not found")

    borrower.deleted_at = datetime.utcnow()
    db.add(borrower)
    await db.commit()
    return None
