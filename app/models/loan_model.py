"""
Modelo de banco de dados para empréstimos de livros.

Define a estrutura da tabela `loans`, relacionando usuários e livros,
com campos de data de empréstimo, devolução e multa.
"""

from sqlalchemy import Column, Date, ForeignKey, Numeric
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.book_model import Book
from app.models.user_model import User
from app.db.base import Base

class Loan(Base):
    """
    Representa um empréstimo de livro realizado por um usuário.

    Atributos:
        id (str): Identificador único do empréstimo (UUID).
        user_id (str): Chave estrangeira para o usuário.
        book_id (str): Chave estrangeira para o livro.
        loan_date (date): Data em que o livro foi emprestado.
        due_date (date): Data prevista para devolução.
        return_date (date | None): Data real da devolução (opcional).
        fine_amount (Decimal): Valor da multa por atraso, se houver.
        user (User): Objeto de relacionamento com o usuário.
        book (Book): Objeto de relacionamento com o livro.
    """
    __tablename__ = "loans"

    id = Column(CHAR(36), primary_key=True, index=True)
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    book_id = Column(CHAR(36), ForeignKey("books.id"), nullable=False)

    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    fine_amount = Column(Numeric(10, 2), default=0.00)

    user = relationship("User", backref="loans")
    book = relationship("Book", backref="loans")
