# test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# Фикстура для тестового клиента
@pytest.fixture
def client():
    """Создаёт тестового клиента для FastAPI приложения."""
    with TestClient(app) as client:
        yield client

# Фикстура для асинхронной сессии базы данных
@pytest.fixture(scope="function")
async def db_session():
    """Создаёт асинхронную сессию базы данных для тестов."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)  # Создаём таблицы
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            yield session
        await connection.run_sync(Base.metadata.drop_all)  # Удаляем таблицы после теста

# Тест создания пользователя
def test_create_user(client):
    """Тестирует создание нового пользователя через API."""
    user_data = {"username": "testuser", "email": "test@example.com"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["username"] == "testuser"
    assert json_response["email"] == "test@example.com"
