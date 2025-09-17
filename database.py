from typing import Any, Generator, AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase, Session

DATABASE_URL = "postgresql+psycopg2://postgres:postgres_password@localhost:5432/postgres_db"
engine = create_async_engine(
    "postgresql+psycopg2://postgres:postgres_password@127.0.0.1:5432/postgres_db"
)
SessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as session:
        yield session