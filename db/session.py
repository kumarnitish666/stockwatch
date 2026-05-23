"""
Database session management.

Sets up the SQLite engine and provides a session factory.
This is the layer that actually talks to the database file.
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db.models import Base

# Database file lives in the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "stockwatch.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# The engine is the entry point to the database. Created once, used forever.
engine = create_engine(DATABASE_URL, echo=False)

# SessionLocal is a "factory" — call it to get a fresh session.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Create all tables defined in models.py if they don't exist yet."""
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DB_PATH}")


def get_session() -> Session:
    """Get a new database session. Caller is responsible for closing it."""
    return SessionLocal()