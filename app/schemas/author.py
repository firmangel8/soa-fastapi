from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema (shared)
class AuthorBase(BaseModel):
    first_name: str
    last_name: str

# Schema for creating new authors (POST)
class AuthorCreate(AuthorBase):
    pass  # author_id auto-generated, so not included

# Schema for updating authors (PUT)
class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# Schema for reading authors (GET responses)
class AuthorRead(AuthorBase):
    author_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
