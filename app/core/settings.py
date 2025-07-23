# app/core/settings.py

from pydantic import BaseSettings, Field

from typing import Optional


class Settings(BaseSettings):
    
    # App
    APP_NAME: str = "Digital Library Management System"
    APP_ENV: str = Field("development", env="APP_ENV")
    DEBUG: bool = Field(True, env="DEBUG")

    # Server
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")

    # Database (MySQL)
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(3306, env="DB_PORT")
    DB_NAME: str = Field("library_db", env="DB_NAME")
    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    # Redis Cache
    REDIS_HOST: str = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")

    # JWT Auth (if used)
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = "app/core/.env"
        env_file_encoding = "utf-8"


settings = Settings()

# Build final SQLALCHEMY_DATABASE_URL if not overridden
if not settings.SQLALCHEMY_DATABASE_URL:
    settings.SQLALCHEMY_DATABASE_URL = (
        f"mysql+pymysql://"
        f"{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
