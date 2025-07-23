"""
Serviços relacionados à autenticação (Auth).

Inclui regras de negócio para:
- Login - Autenticação de usuários
- Verificação de credenciais
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from app.core.security import authenticate_user, create_access_token
from app.core.settings import settings
from app.core.logging import logger


def login_for_access_token_service(    
    db: Session,
    form_data: OAuth2PasswordRequestForm
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

    try:

        logger.info(f"Tentativa de login para o usuário: {form_data}")

        user = authenticate_user(form_data.username, form_data.password, db)        

        # Se o usuário não for encontrado ou a senha estiver incorreta
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

        logger.info(f"Usuário autenticado com sucesso: {user.email}")
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
