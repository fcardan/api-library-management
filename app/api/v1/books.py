"""
API endpoints relacionados à gestão de livros.
"""

from fastapi import APIRouter, Depends, Request, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.models.book_model import Book
from app.schemas.book_schema import BookCreate, BookOut, BookUpdate
from app.dependencies.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.logging import logger
from app.services.book_service import (
    create_book_service,
    get_book_service,
    list_books_service,
    update_book_service,
    delete_book_service,
    list_books_by_availability_service
)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_book(
    request: Request,
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Cadastra um novo livro na base de dados.
    """
    logger.info(f"Criando novo livro: {book.title} | Autor: {book.author_id}")
    try:
        return create_book_service(db, book)
    except HTTPException as e:
        logger.warning(f"Erro ao criar livro: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao criar livro: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar livro")


@router.get("/", response_model=List[BookOut])
@limiter.limit("10/minute")
def list_books(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = Query(None, description="Filtrar por título"),
    author_id: Optional[str] = Query(None, description="Filtrar por ID do autor"),
    order_by: Optional[str] = Query("title", description="Campo de ordenação"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Lista os livros com suporte a paginação, filtro e ordenação.
    """
    logger.debug(f"Listando livros | title={title}, author_id={author_id}, order_by={order_by}")
    try:
        return list_books_service(db, skip, limit, title, author_id, order_by)
    except Exception as e:
        logger.error(f"Erro ao listar livros: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao recuperar livros")





@router.patch("/{book_id}", response_model=BookOut)
@limiter.limit("5/minute")
def patch_book(
    request: Request,
    book_id: str,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Atualiza parcialmente os dados de um livro.
    """
    logger.info(f"Atualizando parcialmente livro ID {book_id}")
    try:
        return update_book_service(db, book_id, book_update, partial=True)
    except HTTPException as e:
        logger.warning(f"Erro ao atualizar livro: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar livro {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar livro")


@router.put("/{book_id}", response_model=BookOut)
@limiter.limit("5/minute")
def put_book(
    request: Request,
    book_id: str,
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Substitui completamente os dados de um livro.
    """
    logger.info(f"Atualizando completamente livro ID {book_id}")
    try:
        return update_book_service(db, book_id, book_data, partial=False)
    except HTTPException as e:
        logger.warning(f"Erro ao substituir livro: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao substituir livro {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao substituir livro")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_book(
    request: Request,
    book_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Remove um livro da base de dados.
    """
    logger.info(f"Excluindo livro ID {book_id}")
    try:
        delete_book_service(db, book_id)
    except HTTPException as e:
        logger.warning(f"Erro ao excluir livro: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao excluir livro {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao excluir livro")


@router.get("/available", response_model=List[BookOut], tags=["Livros"])
def list_books_by_availability(
    request: Request,
    status: bool = Query(..., description="True para disponíveis, False para indisponíveis"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Lista livros disponíveis ou indisponíveis conforme o parâmetro.
    """
    logger.info(f"Listando livros com disponibilidade = {status}")
    try:
        return list_books_by_availability_service(db, status)
    except Exception as e:
        logger.error(f"Erro ao listar livros por disponibilidade: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao recuperar livros")


@router.get("/{book_id}", response_model=BookOut)
def get_book(
    request: Request,
    book_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Busca os detalhes de um livro pelo seu ID.
    """
    logger.debug(f"Buscando livro por ID: {book_id}")
    try:
        return get_book_service(db, book_id)
    except HTTPException as e:
        logger.warning(f"Erro ao buscar livro: {e.detail}")
        raise