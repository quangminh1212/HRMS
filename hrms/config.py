from pathlib import Path
from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = "HRMS"
    db_url: str = "sqlite:///data/hrms.db"  # default dev: SQLite file in data/
    secret_key: str = "change-me"
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None


def load_settings() -> Settings:
    from dotenv import load_dotenv

    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    # Allow DATABASE_URL override for PostgreSQL in prod
    db_url = os.getenv("DATABASE_URL") or os.getenv("DB_URL") or Settings().db_url
    return Settings(
        app_name=os.getenv("APP_NAME", "HRMS"),
        db_url=db_url,
        secret_key=os.getenv("SECRET_KEY", "change-me"),
        smtp_host=os.getenv("SMTP_HOST"),
        smtp_port=int(os.getenv("SMTP_PORT", "0")) or None,
        smtp_user=os.getenv("SMTP_USER"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
    )
