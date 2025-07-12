from sqlalchemy.orm import Session
from uuid import uuid4
from decimal import Decimal
from typing import List
from datetime import date, timedelta

from app.models.loan_model import Loan
from app.models.book_model import Book
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanUpdate, LoanPut
from app.core.logging import logger
from fastapi import HTTPException, status


def create_loan_service(db: Session, loan_data: LoanCreate) -> Loan:
    """
    Cria um novo empréstimo, validando a disponibilidade do livro
    e o limite de empréstimos ativos por usuário.
    """

    user = db.query(User).filter(User.id == str(loan_data.user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    book = db.query(Book).filter(Book.id == str(loan_data.book_id)).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )

    if book.available_copies <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Livro indisponível"
        )

    active_loans = db.query(Loan).filter(
        Loan.user_id == str(loan_data.user_id),
        Loan.return_date == None
    ).count()


    logger.info(f"Usuário {user.email} tem {active_loans} empréstimos ativos")
    # Limite de 3 empréstimos ativos por usuário

    if active_loans >= 3:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Limite de empréstimos ativos atingido"
        )

    loan = Loan(
        id=str(uuid4()),
        user_id=loan_data.user_id,
        book_id=loan_data.book_id,
        loan_date=loan_data.loan_date or date.today(),
        due_date=loan_data.loan_date + timedelta(days=14) if loan_data.loan_date else date.today() + timedelta(days=14),
        fine_amount=Decimal("0.00"),
        return_date=None
    )

    book.available_copies -= 1
    db.add(loan)
    db.commit()
    logger.info(f"Empréstimo criado: {loan.id} para o usuário {loan.user_id} do livro {loan.book_id}")
    db.refresh(loan)
    return loan


def list_loans_service(db: Session) -> List[Loan]:
    """
    Retorna uma lista com todos os empréstimos cadastrados.
    """
    return db.query(Loan).all()


def get_loan_service(db: Session, loan_id: str) -> Loan:
    """
    Busca um empréstimo pelo seu ID.
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado"
        )
    return loan


def update_loan_service(db: Session, loan_id: str, loan_data: LoanPut) -> Loan:
    """
    Substitui completamente os dados de um empréstimo.
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado"
        )

    loan.user_id = loan_data.user_id
    loan.book_id = loan_data.book_id
    loan.loan_date = loan_data.loan_date
    loan.due_date = loan_data.loan_date + timedelta(days=14)
    loan.return_date = loan_data.return_date

    # return_date e multa só se já devolvido
    if loan.return_date and loan.due_date:

        # a data de devolução não pode ser maior que a data atual 
        if loan.return_date > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data de devolução não pode ser no futuro"
            )

        # Se a data de devolução for posterior à data de vencimento, calcula a multa
        if loan.return_date > loan.due_date:

            loan.return_date = loan_data.return_date            
            days_late = (loan.return_date - loan.due_date).days
            loan.fine_amount = Decimal("2.00") * days_late
        else:
            loan.fine_amount = Decimal("0.00")

        # Libera cópia do livro se devolução feita
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            book.available_copies += 1

    else:
        loan.fine_amount = Decimal("0.00")

    db.commit()
    logger.info(f"Empréstimo {loan.id} atualizado com sucesso via PUT")
    db.refresh(loan)
    return loan


def patch_loan_service(db: Session, loan_id: str, loan_data: LoanUpdate) -> Loan:
    """
    Atualiza parcialmente os dados de um empréstimo.
    Se houver devolução, calcula a multa e devolve a cópia do livro.
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado"
        )

    data = loan_data.dict(exclude_unset=True)

    if "user_id" in data:
        loan.user_id = data["user_id"]
    if "book_id" in data:
        loan.book_id = data["book_id"]
    if "loan_date" in data:
        loan.loan_date = data["loan_date"]
    if "due_date" in data:
        loan.due_date = data["due_date"]

    if "return_date" in data:
        loan.return_date = data["return_date"]
        
        # a data de devolução não pode ser maior que a data atual
        if loan.return_date > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data de devolução não pode ser no futuro"
            )
            
        if loan.return_date and loan.due_date:

            # se a data de devolução for posterior à data de vencimento, calcula a multa
            if loan.return_date > loan.due_date:
                days_late = (loan.return_date - loan.due_date).days
                loan.fine_amount = Decimal("2.00") * days_late
            else:
                loan.fine_amount = Decimal("0.00")

        # Libera cópia do livro se devolução feita
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            book.available_copies += 1

    db.commit()
    logger.info(f"Empréstimo {loan.id} atualizado parcialmente com sucesso")
    db.refresh(loan)
    return loan



def delete_loan_service(db: Session, loan_id: str) -> None:
    """
    Remove um empréstimo do banco de dados e devolve o livro se não foi devolvido.
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado"
        )

    if loan.return_date is None:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            book.available_copies += 1

    db.delete(loan)
    db.commit()
    logger.info(f"Empréstimo {loan.id} removido com sucesso")


def list_active_loans_by_user_service(db: Session, user_id: str) -> List[Loan]:
    return db.query(Loan).filter(
        Loan.user_id == user_id,
        Loan.return_date == None
    ).all()


def list_overdue_loans_by_user_service(db: Session, user_id: str) -> List[Loan]:
    today = date.today()
    return db.query(Loan).filter(
        Loan.user_id == user_id,
        Loan.return_date == None,
        Loan.due_date < today
    ).all()


def list_loan_history_by_user_service(db: Session, user_id: str) -> List[Loan]:
    return db.query(Loan).filter(Loan.user_id == user_id).all()
