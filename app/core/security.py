# app/core/security.py

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt

from typing import Optional
from datetime import datetime, timedelta

from app.core.settings import settings
from app.models.user_model import User
from app.dependencies.auth import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera um hash seguro para uma senha."""
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """Valida um usuário com base no email e senha fornecidos."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT com dados e tempo de expiração."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

# ---------- Proteção de rotas com token ----------

