# app/services/report_service.py
from fpdf import FPDF
from sqlalchemy.orm import Session

from datetime import datetime
from typing import List
import csv
import os

from app.models.book_model import Book
from app.models.loan_model import Loan

REPORT_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')
os.makedirs(REPORT_DIR, exist_ok=True)


def fetch_books(db: Session) -> List[Book]:
    return db.query(Book).all()


def fetch_loans(db: Session) -> List[Loan]:
    return db.query(Loan).all()


def export_books_csv(db: Session) -> str:
    books = fetch_books(db)
    filename = os.path.join(REPORT_DIR, f'books_{datetime.now():%Y%m%d_%H%M%S}.csv')
    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Título", "Autor ID", "Publicado em", "Total Cópia", "Disponíveis"])
        for b in books:
            writer.writerow([b.id, b.title, b.author_id, b.published_date, b.total_copies, b.available_copies])
    return filename


def export_report_pdf(db: Session) -> str:
    books = fetch_books(db)
    loans = fetch_loans(db)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Relatório de Livros e Empréstimos', ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, '== Livros ==', ln=True)
    for b in books:
        pdf.cell(0, 6, f'{b.id} | {b.title} | Disponíveis: {b.available_copies}', ln=True)
    pdf.ln(4)

    pdf.cell(0, 8, '== Empréstimos ==', ln=True)
    for ln in loans:
        pdf.cell(0, 6, f'{ln.id} | Usuário: {ln.user_id} | Livro: {ln.book_id} | Empréstimo: {ln.loan_date} | Devolução: {ln.return_date}', ln=True)

    filename = os.path.join(REPORT_DIR, f'report_{datetime.now():%Y%m%d_%H%M%S}.pdf')
    pdf.output(filename)
    return filename