"""
Módulo de rotas para operações relacionadas aos autores.

Inclui criação, listagem, busca por ID, atualização completa/parcial e exclusão.
"""

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from uuid import UUID

from app.db.session import get_db
from app.schemas.author_schema import AuthorCreate, AuthorOut
from app.schemas.book_schema import BookOut
from app.dependencies.auth import get_current_user
from app.services.author_service import (
    create_author_service,
    list_authors_service,
    get_author_service,
    update_author_service,
    patch_author_service,
    delete_author_service
)
from app.models.book_model import Book
from app.models.author_model import Author
from app.core.logging import logger

router = APIRouter()

# Limite de requisições por minuto por IP
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=AuthorOut, status_code=status.HTTP_201_CREATED, tags=["Autores"])
@limiter.limit("20/minute")
def create_author(
    request: Request,
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Cria um novo autor se ainda não existir com o mesmo nome.
    """
    logger.info(f"Solicitada criação de autor: {author.name}")
    return create_author_service(db, author)


@router.get("/{author_id}", response_model=AuthorOut, tags=["Autores"])
@limiter.limit("50/minute")
def get_author(
    request: Request,
    author_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Busca os detalhes de um autor pelo seu ID.
    """
    logger.debug(f"Solicitada busca de autor ID: {author_id}")
    return get_author_service(db, author_id)


@router.get("/", response_model=list[AuthorOut], tags=["Autores"])
@limiter.limit("50/minute")
def list_authors(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retorna a lista completa de autores cadastrados.
    """
    logger.debug("Solicitada listagem de autores")
    return list_authors_service(db)


@router.get("/{author_id}/books", response_model=list[BookOut], tags=["Autores"])
@limiter.limit("50/minute")
def list_books_by_author(
    request: Request,
    author_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retorna todos os livros associados a um autor específico.
    """
    logger.debug(f"Solicitada listagem de livros para o autor ID: {author_id}")

    author = db.query(Author).filter(Author.id == str(author_id)).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado"
        )

    books = db.query(Book).filter(Book.author_id == str(author_id)).all()
    logger.info(f"{len(books)} livros encontrados para o autor {author.name}")
    return books


@router.put("/{author_id}", response_model=AuthorOut, tags=["Autores"])
@limiter.limit("20/minute")
def update_author(
    request: Request,
    author_id: UUID,
    author_update: AuthorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Atualiza completamente os dados de um autor.
    """
    logger.info(f"Solicitada atualização total do autor ID: {author_id}")
    return update_author_service(db, str(author_id), author_update)


@router.patch("/{author_id}", response_model=AuthorOut, tags=["Autores"])
@limiter.limit("20/minute")
def patch_author(
    request: Request,
    author_id: UUID,
    author_update: AuthorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Atualiza parcialmente os dados de um autor.
    """
    logger.info(f"Solicitada atualização parcial do autor ID: {author_id}")
    return patch_author_service(db, str(author_id), author_update)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Autores"])
@limiter.limit("20/minute")
def delete_author(
    request: Request,
    author_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Remove um autor do sistema pelo seu ID.
    """
    logger.info(f"Solicitada exclusão do autor ID: {author_id}")
    delete_author_service(db, str(author_id))
    return None

