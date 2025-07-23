"""
Módulo de autenticação da API.

Fornece endpoint para login e geração de token JWT para usuários autenticados.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.session import get_db
from app.core.logging import logger
from app.services.auth_service import login_for_access_token_service

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/token", summary="Autenticação do usuário (Login)")
@limiter.limit("7/minute")
def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Realiza a autenticação do usuário e retorna um token JWT válido.

    Este endpoint utiliza o padrão OAuth2 com fluxo de "password".

    Parâmetros:
    - **form_data**: formulário contendo `username` (email) e `password`.
    - **db**: instância da sessão do banco de dados.

    Retorno:
    - Token JWT de acesso com tempo de expiração definido nas configurações.
    """
    logger.info(f"Tentando autenticar usuário: {form_data.username}")
    return login_for_access_token_service(db, form_data)
