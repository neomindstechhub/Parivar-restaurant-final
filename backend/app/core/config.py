import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Parivar Restaurant OS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Supports both SQLite (local) and PostgreSQL (production)
    # Set DATABASE_URL in your environment for production:
    #   postgresql+asyncpg://user:pass@host:port/dbname
    DATABASE_URL: str = "sqlite+aiosqlite:///./parivar.db"

    # JWT Settings
    SECRET_KEY: str = "parivar_super_secret_key_for_development_only_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS — comma-separated list of allowed frontend origins
    # e.g. "https://parivar.vercel.app,https://yourdomain.com"
    CORS_ORIGINS: str = "*"

    class Config:
        case_sensitive = True
        env_file = (".env", "../.env")
        extra = "ignore"

settings = Settings()
