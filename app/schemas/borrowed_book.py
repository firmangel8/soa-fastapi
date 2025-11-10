from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Shared schema
class BorrowedBookBase(BaseModel):
    book_id: Optional[int] = None
    borrower_id: Optional[int] = None
    borrow_date: Optional[date] = None
    return_date: Optional[date] = None


# Create (POST)
class BorrowedBookCreate(BorrowedBookBase):
    pass


# Update (PUT)
class BorrowedBookUpdate(BaseModel):
    book_id: Optional[int] = None
    borrower_id: Optional[int] = None
    borrow_date: Optional[date] = None
    return_date: Optional[date] = None


# Read (GET response)
class BorrowedBookRead(BorrowedBookBase):
    borrow_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
