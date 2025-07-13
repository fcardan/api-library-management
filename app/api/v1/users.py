"""
Rotas relacionadas aos usuários.

Inclui operações de criação, listagem, detalhamento, atualização e remoção
de usuários do sistema com autenticação e validações apropriadas.
"""

from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List

from app.db.session import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate
from app.dependencies.auth import get_current_user
from app.services.user_service import (
    create_user_service,
    list_users_service,
    get_user_service,
    update_user_service,
    delete_user_service
)
from app.core.logging import logger

router = APIRouter()

# Limite de requisições por minuto por IP
limiter = Limiter(key_func=get_remote_address)  # por IP


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["Usuários"])
@limiter.limit("20/minute")
def create_user(
    request: Request, user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema, caso o e-mail ainda não esteja em uso.
    """
    logger.info("Tentando criar um novo usuário")
    return create_user_service(db, user_in)


@router.get("/", response_model=List[UserOut], tags=["Usuários"])
@limiter.limit("50/minute")
def list_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna a lista de todos os usuários cadastrados.
    Requer autenticação.
    """
    logger.info(f"Usuário {current_user.email} solicitou a listagem de usuários")
    return list_users_service(db)


@router.get("/{user_id}", response_model=UserOut, tags=["Usuários"])
@limiter.limit("50/minute")
def get_user(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna os dados de um usuário específico pelo seu ID.
    Requer autenticação.
    """
    logger.info(f"Usuário {current_user.email} solicitou dados do usuário ID: {user_id}")
    return get_user_service(db, user_id)


@router.get("/{user_id}/loans", response_model=UserOut, tags=["Usuários"])
@limiter.limit("50/minute")
def get_loans(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna lista de empréstimos de um usuário específico pelo seu ID.
    Requer autenticação.
    """
    from app.models.loan_model import Loan  # Evita import circular
    logger.info(f"Usuário {current_user.email} solicitou lista de empréstimos do usuário ID: {user_id}")

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


@router.put("/{user_id}", response_model=UserOut, tags=["Usuários"])
@limiter.limit("20/minute")
def update_user(
    request: Request,
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza completamente os dados de um usuário.
    """
    logger.info(f"Usuário {current_user.email} solicitou atualização completa de usuário ID: {user_id}")
    return update_user_service(db, user_id, user_update)


@router.patch("/{user_id}", response_model=UserOut, tags=["Usuários"])
@limiter.limit("20/minute")
def patch_user(
    request: Request,
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza parcialmente os dados de um usuário.
    """
    logger.info(f"Usuário {current_user.email} solicitou atualização parcial de usuário ID: {user_id}")
    return update_user_service(db, user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuários"])
@limiter.limit("20/minute")
def delete_user(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um usuário do sistema pelo seu ID.
    """
    logger.info(f"Usuário {current_user.email} solicitou remoção do usuário ID: {user_id}")
    delete_user_service(db, user_id)
    return None
