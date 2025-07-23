# app/api/v1/reports.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

import os

from app.db.session import get_db
from app.services.report_service import export_books_csv, export_report_pdf

router = APIRouter()

# Limite de requisições por minuto por IP
limiter = Limiter(key_func=get_remote_address)  # por IP

@router.get('/books/csv', summary='Exportar relatório de livros em CSV')
def get_books_csv(db: Session = Depends(get_db)):
    try:
        file_path = export_books_csv(db)
        return FileResponse(path=file_path, media_type='text/csv', filename=os.path.basename(file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/full/pdf', summary='Exportar relatório completo em PDF')
def get_full_pdf(db: Session = Depends(get_db)):
    try:
        file_path = export_report_pdf(db)
        return FileResponse(path=file_path, media_type='application/pdf', filename=os.path.basename(file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
