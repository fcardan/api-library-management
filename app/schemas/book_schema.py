"""
Schemas para operações com livros.

Define os modelos Pydantic utilizados para validação e serialização
de dados relacionados aos livros cadastrados no sistema.
"""

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    """
    Representa os campos básicos de um livro.
    Utilizado como base para criação e leitura.
    """
    title: str = Field(..., max_length=200, description="Título do livro")
    author_id: UUID = Field(..., description="ID do autor do livro")
    published_date: date = Field(..., description="Data de publicação")
    total_copies: int = Field(..., ge=1, description="Total de cópias cadastradas")


class BookCreate(BookBase):
    """
    Modelo para criação de um novo livro.
    Inclui o número de cópias disponíveis.
    """
    available_copies: int = Field(..., ge=0, description="Número de cópias disponíveis")


class BookOut(BookBase):
    """
    Modelo de saída (response) com os dados públicos de um livro.
    Inclui o ID e o número de cópias disponíveis.
    """
    id: UUID
    available_copies: int

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    """
    Modelo para atualização parcial ou completa de um livro.
    Todos os campos são opcionais para permitir PATCH ou PUT.
    """
    title: Optional[str] = Field(None, max_length=200, description="Título do livro")
    author_id: Optional[UUID] = Field(None, description="ID do autor do livro")
    published_date: Optional[date] = Field(None, description="Data de publicação")
    total_copies: Optional[int] = Field(None, ge=1, description="Total de cópias cadastradas")
    available_copies: Optional[int] = Field(None, ge=0, description="Número de cópias disponíveis")

    class Config:
        orm_mode = True
