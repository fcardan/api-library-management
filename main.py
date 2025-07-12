from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.core.settings import settings
from app.api.v1.router import api_router as v1_router

app = FastAPI(
    title=settings.APP_NAME,
    description="API RESTful para gerenciamento de biblioteca digital com controle de usuários, livros e empréstimos.",
    version=settings.API_VERSION if hasattr(settings, "API_VERSION") else "1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# OAuth2 para Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Inclui o router com prefixo /api/v1
app.include_router(v1_router, prefix="/api/v1")

@app.get("/", tags=["Health"], summary="Verifica status da API", description="Endpoint de verificação básica para confirmar que a API está operando.")
def read_root():
    return {"status": "API is running"}
