import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Добавляем корень проекта в sys.path для корректного импорта 'main'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import app
from database import Base, get_session
from models.authors import Author
from models.quotes import Quote


# Создаем отдельный in-memory SQLite для тестов, общий для всех соединений
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)


# Для SQLite необходимо включить поддержку внешних ключей
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def override_get_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client():
    # Чистая БД перед каждым тестом
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session(client):
    # отдаём отдельную сессию для прямой записи стартовых данных
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


@pytest.fixture()
def author_factory(db_session):
    def _create_author(**kwargs):
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_year": 1900,
        }
        payload.update(kwargs)
        obj = Author(**payload)
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        return obj
    return _create_author


@pytest.fixture()
def quote_factory(db_session, author_factory):
    def _create_quote(**kwargs):
        if "author_id" not in kwargs:
            author = author_factory()
            kwargs["author_id"] = author.id
        payload = {
            "text": "Sample quote",
            "author_id": kwargs["author_id"],
        }
        payload.update(kwargs)
        obj = Quote(**payload)
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        return obj
    return _create_quote
