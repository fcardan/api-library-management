"""
Serviço de livros contendo regras de negócio para criação,
busca, listagem, atualização (completa e parcial) e remoção de livros.
"""

from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi import HTTPException, status
from typing import Optional, List
from app.models.book_model import Book
from app.schemas.book_schema import BookCreate, BookUpdate
from app.core.logging import logger

def create_book_service(db: Session, book_data: BookCreate) -> Book:
    """
    Cria um novo livro no banco de dados com validações.
    """
    # Verifica existência do autor
    author_exists = db.query("Author").filter_by(id=str(book_data.author_id)).first()
    if not author_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado")

    # Verifica duplicidade de título com autor diferente
    existing_book = db.query(Book).filter(Book.title == book_data.title).first()
    if existing_book:
        if existing_book.author_id != str(book_data.author_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um livro com esse título vinculado a outro autor"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um livro com esse título."
            )

    if book_data.total_copies < 0 or book_data.available_copies < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Número de cópias não pode ser negativo"
        )

    if book_data.available_copies > book_data.total_copies:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cópias disponíveis não podem ser maiores que o total"
        )

    book = Book(
        id=str(uuid4()),
        title=book_data.title,
        author_id=str(book_data.author_id),
        published_date=book_data.published_date,
        total_copies=book_data.total_copies,
        available_copies=book_data.available_copies,
    )
    db.add(book)
    db.commit()
    logger.info(f"Livro {book.title} criado com sucesso")
    db.refresh(book)
    return book


def get_book_service(db: Session, book_id: str) -> Book:
    """
    Busca um livro pelo seu ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    return book


def list_books_service(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    author_id: Optional[str] = None,
    order_by: Optional[str] = "title"
) -> List[Book]:
    """
    Retorna livros cadastrados com paginação, filtro e ordenação.
    """
    query = db.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author_id:
        query = query.filter(Book.author_id == author_id)
    if order_by in ["title", "published_date", "total_copies"]:
        query = query.order_by(getattr(Book, order_by))

    return query.offset(skip).limit(limit).all()


def update_book_service(
    db: Session,
    book_id: str,
    book_data: BookUpdate,
    partial: bool = True
) -> Book:
    """
    Atualiza os dados de um livro existente.
    Se partial=True, faz update parcial; caso contrário, substitui completamente.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")

    # Validações
    total_copies = None
    available_copies = None

    if partial:
        data = book_data.dict(exclude_unset=True)
        total_copies = data.get("total_copies", book.total_copies)
        available_copies = data.get("available_copies", book.available_copies)
    else:
        # Substituição completa, book_data é BookCreate (todos os campos obrigatórios)
        total_copies = book_data.total_copies
        available_copies = book_data.available_copies

    if total_copies < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Total de cópias não pode ser negativo")
    if available_copies < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cópias disponíveis não podem ser negativas")
    if available_copies > total_copies:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cópias disponíveis não podem ser maiores que o total")

    # Atualiza os campos
    if partial:
        for field, value in data.items():
            setattr(book, field, value)
    else:
        # substitui todos os campos
        book.title = book_data.title
        book.author_id = str(book_data.author_id)
        book.published_date = book_data.published_date
        book.total_copies = book_data.total_copies
        book.available_copies = book_data.available_copies

    db.commit()
    logger.info(f"Livro {book.title} atualizado com sucesso")
    db.refresh(book)
    return book


def delete_book_service(db: Session, book_id: str) -> None:
    """
    Remove um livro do banco de dados, se possível.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")

    if book.available_copies < book.total_copies:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir livro com cópias emprestadas"
        )

    db.delete(book)
    db.commit()
    logger.info(f"Livro {book.title} removido com sucesso")


def list_books_by_availability_service(db: Session, status: bool) -> List[Book]:
    """
    Lista livros disponíveis ou indisponíveis conforme parâmetro.
    """
    if status:
        return db.query(Book).filter(Book.available_copies > 0).all()
    else:
        return db.query(Book).filter(Book.available_copies == 0).all()
