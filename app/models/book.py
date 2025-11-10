from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Book(Base):
    __tablename__ = "tb_books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey("tb_authors.author_id"), nullable=True)
    publication_year = Column(Integer, nullable=True)
    genre = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    author = relationship("Author", back_populates="books")
