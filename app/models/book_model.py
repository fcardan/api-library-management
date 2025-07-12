"""
Modelo de banco de dados para livros da biblioteca.

Define a estrutura da tabela `books`, incluindo campos como
título, autor, datas e controle de cópias.
"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from app.models.author_model import Author
from app.db.base import Base

class Book(Base):
    """
    Representa um livro no sistema da biblioteca.

    Atributos:
        id (str): Identificador único do livro (UUID).
        title (str): Título do livro.
        author_id (str): Chave estrangeira para o autor do livro.
        published_date (date): Data de publicação do livro.
        available_copies (int): Quantidade de cópias disponíveis para empréstimo.
        total_copies (int): Quantidade total de cópias cadastradas.
        author (Author): Objeto de relacionamento com o autor.
    """
    __tablename__ = "books"

    id = Column(CHAR(36), primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author_id = Column(CHAR(36), ForeignKey("authors.id"), nullable=False)
    published_date = Column(Date)
    available_copies = Column(Integer, default=0)
    total_copies = Column(Integer, default=1)

    author = relationship("Author", backref="books")
