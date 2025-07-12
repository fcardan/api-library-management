from fastapi import APIRouter
from app.api.v1 import users, books, loans, auth, authors

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Usuários"])
api_router.include_router(books.router, prefix="/books", tags=["Livros"])
api_router.include_router(loans.router, prefix="/loans", tags=["Empréstimos"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(authors.router, prefix="/authors", tags=["Autores"])
