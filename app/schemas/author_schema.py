"""
Schemas para operações com autores.

Define os modelos Pydantic utilizados para validação e serialização
de dados relacionados a autores no sistema, incluindo criação e leitura.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class AuthorBase(BaseModel):
    """
    Representa os campos básicos de um autor.
    Utilizado como base para criação e leitura.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Nome do autor")
    bio: Optional[str] = Field(None, max_length=500, description="Biografia do autor")


class AuthorCreate(AuthorBase):
    """
    Modelo para criação de um novo autor.
    Herda todos os campos de AuthorBase.
    """
    pass


class AuthorOut(AuthorBase):
    """
    Modelo de saída (response) com os dados públicos de um autor.
    Inclui o identificador único (UUID).
    """
    id: UUID

    class Config:
        orm_mode = True

class AuthorUpdate(BaseModel):
    """
    Modelo para atualização parcial ou completa de um autor.
    Todos os campos são opcionais para permitir PATCH ou PUT.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nome do autor")
    bio: Optional[str] = Field(None, max_length=500, description="Biografia do autor")

    class Config:
        orm_mode = True
