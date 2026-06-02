"""Application configuration.

Sensitive values come from environment variables. The default database is SQLite
so the project works immediately for students. For PostgreSQL, set DATABASE_URL
in .env, for example:
postgresql://username:password@localhost:5432/mkulima_chapchap
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base Flask configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mkulima_chapchap.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
