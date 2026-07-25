from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import Generator

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()