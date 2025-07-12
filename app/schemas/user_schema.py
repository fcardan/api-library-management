"""
Schemas para operações com usuários.

Contém os modelos Pydantic utilizados para validação e serialização
de dados relacionados a usuários no sistema, incluindo criação,
leitura e atualização.
"""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """
    Representa os campos básicos de um usuário.
    Utilizado como base para criação, leitura e atualização.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Nome do usuário")
    email: EmailStr = Field(..., description="Endereço de e-mail do usuário")


class UserCreate(UserBase):
    """
    Modelo para criação de um novo usuário.
    Herda os campos de UserBase e adiciona a senha.
    """
    password: str = Field(..., min_length=8, max_length=128, description="Senha do usuário")


class UserUpdate(BaseModel):
    """
    Modelo para atualização parcial ou total de um usuário.
    Todos os campos são opcionais.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Novo nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Novo e-mail do usuário")
    password: Optional[str] = Field(None, min_length=8, max_length=128, description="Nova senha do usuário")


class UserOut(UserBase):
    """
    Modelo de saída (response) para exibir dados públicos de um usuário.
    Inclui o ID e a data de criação.
    """
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
