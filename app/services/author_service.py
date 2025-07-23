"""
Serviços relacionados à entidade Author.

Inclui regras de negócio para:
- Criar autor
- Listar autores
- Buscar por ID
- Atualizar autor (PUT)
- Atualizar parcial (PATCH)
- Deletar autor
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from uuid import uuid4

from app.models.author_model import Author
from app.schemas.author_schema import AuthorCreate
from app.core.logging import logger


def create_author_service(db: Session, author_data: AuthorCreate) -> Author:
    """
    Cria um novo autor no banco de dados, evitando duplicidade pelo nome.
    """
    existing_author = db.query(Author).filter(Author.name == author_data.name).first()
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Autor já cadastrado"
        )

    new_author = Author(
        id=str(uuid4()),
        name=author_data.name,
        bio=author_data.bio or None
    )
    db.add(new_author)
    db.commit()
    logger.info(f"Autor {new_author.name} criado com sucesso")
    db.refresh(new_author)
    return new_author


def list_authors_service(db: Session) -> list[Author]:
    """
    Lista todos os autores cadastrados.
    """
    return db.query(Author).all()


def get_author_service(db: Session, author_id: str) -> Author:
    """
    Busca um autor pelo ID.
    """
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado"
        )
    return author


def update_author_service(db: Session, author_id: str, author_data: AuthorCreate) -> Author:
    """
    Atualiza completamente os dados de um autor existente.
    """
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado"
        )

    author.name = author_data.name
    author.bio = author_data.bio
    db.commit()
    logger.info(f"Autor {author.name} atualizado com sucesso")
    db.refresh(author)
    return author

def patch_author_service(db: Session, author_id: str, author_data: AuthorCreate) -> Author:
    """
    Atualiza parcialmente os dados de um autor.
    """
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado"
        )

    if author_data.name is not None:
        author.name = author_data.name
    if author_data.bio is not None:
        author.bio = author_data.bio

    db.commit()
    logger.info(f"Autor {author.name} atualizado parcialmente com sucesso")
    db.refresh(author)
    return author


def delete_author_service(db: Session, author_id: str) -> None:
    """
    Remove um autor do banco de dados.
    """
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado"
        )

    db.delete(author)
    db.commit()
    logger.info(f"Autor {author.name} removido com sucesso")
