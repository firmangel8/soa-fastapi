from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime
from app.core.database import Base

class Borrower(Base):
    __tablename__ = "tb_borrowers"

    borrower_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
