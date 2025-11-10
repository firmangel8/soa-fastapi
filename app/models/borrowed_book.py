from sqlalchemy import Column, Integer, Date, TIMESTAMP, ForeignKey
from datetime import datetime
from app.core.database import Base

class BorrowedBook(Base):
    __tablename__ = "tb_borrowed_books"

    borrow_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("tb_books.book_id"), nullable=True)
    borrower_id = Column(Integer, ForeignKey("tb_borrowers.borrower_id"), nullable=True)
    borrow_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
