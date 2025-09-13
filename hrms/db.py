from .config import load_settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

settings = load_settings()

# Ensure data directory exists for SQLite
if settings.db_url.startswith("sqlite"):
    Path("data").mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.db_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()
