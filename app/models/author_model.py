"""
Modelo de banco de dados para autores da biblioteca.

Define a estrutura da tabela `authors`, armazenando informações
como nome e biografia do autor.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import CHAR
from app.db.base import Base

class Author(Base):
    """
    Representa um autor de livros cadastrados na biblioteca.

    Atributos:
        id (str): Identificador único do autor (UUID em formato string).
        name (str): Nome completo do autor.
        bio (str | None): Texto opcional com biografia ou informações adicionais.
    """
    __tablename__ = "authors"

    id = Column(CHAR(36), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
