from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.db.session import SessionLocal
from app.models.user_model import User

# Define o esquema OAuth2 com token do tipo Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Contexto do algoritmo de hash das senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- Funções auxiliares ----------

def get_db():
    """Fornece uma instância da sessão do banco para dependências."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca um usuário no banco de dados pelo email."""
    return db.query(User).filter(User.email == email).first()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Valida e retorna o usuário autenticado com base no token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user
