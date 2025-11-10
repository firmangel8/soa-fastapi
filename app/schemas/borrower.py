from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Shared schema
class BorrowerBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None


# POST (create)
class BorrowerCreate(BorrowerBase):
    pass


# PUT (update)
class BorrowerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


# GET (response)
class BorrowerRead(BorrowerBase):
    borrower_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
