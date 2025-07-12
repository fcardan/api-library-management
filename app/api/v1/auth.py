"""
Módulo de autenticação da API.

Fornece endpoint para login e geração de token JWT para usuários autenticados.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import authenticate_user, create_access_token
from app.db.session import get_db
from app.core.settings import settings
from app.core.logging import logger, success

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/token", summary="Autenticação do usuário (Login)")
@limiter.limit("5/minute")
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

    try:
        user = authenticate_user(form_data.username, form_data.password, db)

        if not user:
            logger.warning(f"Falha de autenticação para o e-mail: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        success(f"Usuário autenticado com sucesso: {user.email}")

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise  # Repassa a exceção já formatada
    except Exception as e:
        logger.error(f"Erro inesperado durante login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar login"
        )
