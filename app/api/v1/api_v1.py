from fastapi import APIRouter
from app.api.v1.routes import user, item, authors, books, borrowers, borrowed_books

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(item.router, prefix="/items", tags=["Items"])
api_router.include_router(authors.router, prefix="/authors", tags=["Authors"])
api_router.include_router(books.router, prefix="/books", tags=["Books"])
api_router.include_router(borrowers.router, prefix="/borrowers", tags=["Borrowers"])
api_router.include_router(borrowed_books.router, prefix="/borrowed-books", tags=["Borrowed Books"])
