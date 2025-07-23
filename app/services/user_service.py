from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from uuid import uuid4
from typing import List

from app.models.user_model import User
from app.models.loan_model import Loan
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.core.logging import logger



def create_user_service(db: Session, user_data: UserCreate) -> User:
    """
    Cria um novo usuário no banco de dados.
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado"
        )

    hashed_pw = get_password_hash(user_data.password)

    new_user = User(
        id=str(uuid4()),
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    logger.info(f"Usuário {new_user.email} criado com sucesso")
    db.refresh(new_user)
    return new_user


def list_users_service(db: Session) -> List[User]:
    """
    Retorna uma lista com todos os usuários cadastrados.
    """
    return db.query(User).all()


def get_user_service(db: Session, user_id: str) -> User:
    """
    Busca um usuário pelo ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user


def get_user_loans_service(db: Session, user_id: str) -> List[Loan]:
    """
    Retorna os empréstimos de um usuário específico.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    if not loans:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum empréstimo encontrado para este usuário"
        )

    return loans


def update_user_service(db: Session, user_id: str, user_data: UserUpdate) -> User:
    """
    Atualiza os dados de um usuário existente (PUT/PATCH).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    if user_data.email and user.email != user_data.email:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado"
            )
        user.email = user_data.email

    if user_data.name:
        user.name = user_data.name

    if user_data.password:
        user.hashed_password = get_password_hash(user_data.password)

    db.commit()
    logger.info(f"Usuário {user.email} atualizado com sucesso")
    db.refresh(user)
    return user


def delete_user_service(db: Session, user_id: str) -> None:
    """
    Remove um usuário do banco de dados.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    db.delete(user)
    db.commit()
    logger.info(f"Usuário {user.email} removido com sucesso")
