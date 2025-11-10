from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.core.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "tb_authors"

    author_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
