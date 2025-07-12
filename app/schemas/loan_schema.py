"""
Schemas para operações com empréstimos de livros.

Define os modelos Pydantic utilizados para validação e serialização
de dados relacionados aos empréstimos registrados no sistema.
"""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from decimal import Decimal
from typing import Optional


class LoanBase(BaseModel):
    """
    Representa os campos básicos de um empréstimo.
    Utilizado como base para leitura e escrita.
    """
    user_id: UUID = Field(..., description="ID do usuário que realizou o empréstimo")
    book_id: UUID = Field(..., description="ID do livro emprestado")
    loan_date: date = Field(..., description="Data do empréstimo")

class LoanCreate(LoanBase):
    """
    Modelo para criação de um novo empréstimo.
    Permite que loan_date e due_date sejam opcionais, pois o serviço os calcula.
    """    
    pass

class LoanPut(BaseModel):
    user_id: UUID
    book_id: UUID
    loan_date: date
    due_date: date
    return_date: Optional[date] = None

    class Config:
        orm_mode = True


class LoanOut(LoanBase):
    """
    Modelo de saída com os dados completos de um empréstimo.
    Inclui ID, data de devolução e valor da multa, se houver.
    """
    id: UUID
    due_date: date = Field(..., description="Data de vencimento do empréstimo")
    return_date: Optional[date] = Field(None, description="Data de devolução, se houver")
    fine_amount: Decimal = Field(..., ge=0, description="Valor da multa, se houver")

    class Config:
        orm_mode = True

class LoanUpdate(BaseModel):
    """
    Modelo para atualização de um empréstimo.

    Permite atualizar a data de devolução, data de vencimento e valor da multa.
    Todos os campos são opcionais para suportar operações do tipo PATCH.
    """
    return_date: Optional[date] = Field(None, description="Nova data de devolução")
    due_date: Optional[date] = Field(None, description="Nova data de vencimento")    

    class Config:
        orm_mode = True

