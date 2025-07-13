"""
Rotas relacionadas a empréstimos de livros.

Permite criar, listar, atualizar, editar parcialmente e remover registros de empréstimos,
incluindo regras de negócio como limite de empréstimos por usuário, cálculo de multas etc.
"""

from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List
from app.db.session import get_db
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanOut, LoanUpdate, LoanPut
from app.dependencies.auth import get_current_user
from app.core.logging import logger
from app.services.loan_service import (
    create_loan_service,
    list_loans_service,
    get_loan_service,
    patch_loan_service,
    update_loan_service,
    delete_loan_service,
    list_active_loans_by_user_service,
    list_overdue_loans_by_user_service,
    list_loan_history_by_user_service
)

router = APIRouter()

# Limite de requisições por minuto por IP
limiter = Limiter(key_func=get_remote_address)  # por IP

@router.post("/", response_model=LoanOut, status_code=status.HTTP_201_CREATED, tags=["Empréstimos"])
@limiter.limit("20/minute")
def create_loan(
    request: Request,
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo empréstimo para um usuário, aplicando as regras de negócio.
    """
    logger.info(f"Usuário {current_user.email} solicitou criação de empréstimo")
    return create_loan_service(db, loan)

@router.get("/{loan_id}", response_model=LoanOut, tags=["Empréstimos"])
@limiter.limit("50/minute")
def get_loan(   
    request: Request,
    loan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna os detalhes de um empréstimo específico.
    """
    logger.info(f"Usuário {current_user.email} solicitou detalhes do empréstimo ID: {loan_id}")
    return get_loan_service(db, loan_id)


@router.get("/", response_model=List[LoanOut], tags=["Empréstimos"])
@limiter.limit("50/minute")
def list_loans(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os empréstimos registrados no sistema.
    """
    logger.info(f"Usuário {current_user.email} solicitou listagem de todos os empréstimos")
    return list_loans_service(db)


@router.get("/active/{user_id}", response_model=List[LoanOut], tags=["Empréstimos"])
@limiter.limit("50/minute")
def list_active_loans(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista os empréstimos ativos (não devolvidos) de um usuário.
    """
    logger.info(f"Usuário {current_user.email} solicitou empréstimos ativos do usuário {user_id}")
    return list_active_loans_by_user_service(db, user_id)


@router.get("/overdue/{user_id}", response_model=List[LoanOut], tags=["Empréstimos"])
@limiter.limit("50/minute")
def list_overdue_loans(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista os empréstimos atrasados de um usuário.
    """
    logger.info(f"Usuário {current_user.email} solicitou empréstimos atrasados do usuário {user_id}")
    return list_overdue_loans_by_user_service(db, user_id)


@router.get("/history/{user_id}", response_model=List[LoanOut], tags=["Empréstimos"])
@limiter.limit("50/minute")
def list_loan_history(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista o histórico completo de empréstimos de um usuário.
    """
    logger.info(f"Usuário {current_user.email} solicitou histórico de empréstimos do usuário {user_id}")
    return list_loan_history_by_user_service(db, user_id)


@router.patch("/{loan_id}", response_model=LoanOut, tags=["Empréstimos"])
@limiter.limit("20/minute")
def patch_loan(
    request: Request,
    loan_id: str,
    loan_data: LoanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza parcialmente os dados de um empréstimo, como data de devolução ou multa.
    """
    logger.info(f"Usuário {current_user.email} solicitou atualização parcial do empréstimo ID: {loan_id}")
    return patch_loan_service(db, loan_id, loan_data)


@router.put("/{loan_id}", response_model=LoanOut, tags=["Empréstimos"])
@limiter.limit("20/minute")
def update_loan(
    request: Request,
    loan_id: str,
    loan_data: LoanPut,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza completamente os dados de um empréstimo.
    """
    logger.info(f"Usuário {current_user.email} solicitou atualização completa do empréstimo ID: {loan_id}")
    return update_loan_service(db, loan_id, loan_data)

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Empréstimos"])
@limiter.limit("20/minute")
def delete_loan(
    request: Request,
    loan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um empréstimo do sistema.
    """
    logger.info(f"Usuário {current_user.email} solicitou exclusão do empréstimo ID: {loan_id}")
    delete_loan_service(db, loan_id)
    return None
