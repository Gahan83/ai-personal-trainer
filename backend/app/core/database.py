"""
Database setup: SQLAlchemy engine, session factory, declarative base, and a
FastAPI dependency for per-request sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Render/Heroku hand out URLs starting with "postgres://"; SQLAlchemy 2.x wants
# "postgresql://". Normalise so the same env var works everywhere.
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# check_same_thread=False is required for SQLite with FastAPI's threadpool.
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

# pool_pre_ping avoids stale connections being recycled by managed Postgres.
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency yielding a DB session, closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
