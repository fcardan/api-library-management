"""
Modelo de banco de dados para usuários da biblioteca.

Define a estrutura da tabela `users`, incluindo campos
como nome, e-mail, senha criptografada e data de criação.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, timezone
from app.db.base import Base

class User(Base):
    """
    Representa um usuário no sistema da biblioteca.

    Atributos:
        id (str): Identificador único (UUID) do usuário.
        name (str): Nome completo do usuário.
        email (str): Endereço de e-mail do usuário (único).
        hashed_password (str): Senha do usuário criptografada.
        created_at (datetime): Data de criação do registro.
    """
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
