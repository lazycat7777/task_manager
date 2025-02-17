import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import random
import string


@pytest.fixture(scope="module")
def client():
    """Создает тестового клиента для FastAPI приложения.

    Этот клиент будет использоваться для выполнения HTTP-запросов в рамках
    тестов. Он позволяет симулировать работу с API приложения без необходимости
    запускать сервер.

    Returns:
        TestClient: Клиент для отправки запросов в FastAPI приложение.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module", autouse=True)
async def db_session():
    """Создает асинхронную сессию базы данных для тестов на уровне модуля.

    Эта фикстура используется для настройки базы данных перед выполнением тестов
    и для очистки базы данных после завершения тестов. Она инициализирует базу
    данных, создает таблицы и выполняет все необходимые операции с сессией базы данных.

    Yields:
        AsyncSession: Асинхронная сессия для работы с базой данных.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
def created_user(client):
    """Создает тестового пользователя для использования в тестах.

    Генерирует случайный суффикс для имени пользователя и email, чтобы
    обеспечить уникальность данных. Этот пользователь будет создан один раз
    для всех тестов в модуле.

    Args:
        client (TestClient): Тестовый клиент для взаимодействия с API.

    Returns:
        dict: Данные созданного пользователя.
    """
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=5))
    user_data = {
        "username": f"testuser_{random_suffix}",
        "email": f"test_{random_suffix}@example.com"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture(scope="module")
def created_task(client, created_user):
    """Создает тестовую задачу, привязанную к созданному пользователю.

    Задача будет создана один раз для всех тестов в модуле и будет привязана
    к пользователю, созданному с помощью фикстуры created_user.

    Args:
        client (TestClient): Тестовый клиент для взаимодействия с API.
        created_user (dict): Данные пользователя, к которому привязывается задача.

    Returns:
        dict: Данные созданной задачи.
    """
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2025-01-01",
        "user_id": created_user["id"]
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201, response.text
    return response.json()


def test_create_user(created_user):
    """Тестирование создания пользователя.

    Проверяет, что пользователь был успешно создан и что его данные
    (username и email) соответствуют отправленным.

    Args:
        created_user (dict): Данные созданного пользователя.
    """
    assert "id" in created_user
    assert "username" in created_user
    assert "email" in created_user

    assert created_user["username"].startswith("testuser_")
    assert created_user["email"].startswith("test_")


def test_read_user(client, created_user):
    """Тестирование получения данных пользователя по его ID.

    Проверяет, что при запросе данных пользователя по ID, возвращаются
    корректные данные (username и email).

    Args:
        client (TestClient): Тестовый клиент для взаимодействия с API.
        created_user (dict): Данные созданного пользователя.
    """
    user_id = created_user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert json_response["username"] == created_user["username"]
    assert json_response["email"] == created_user["email"]


def test_create_task(created_task):
    """Тестирование создания задачи.

    Проверяет, что задача была успешно создана и что её данные (title и description)
    соответствуют отправленным.

    Args:
        created_task (dict): Данные созданной задачи.
    """
    assert "id" in created_task
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "This is a test task"


def test_read_tasks(client, created_user, created_task):
    """Тестирование получения всех задач пользователя.

    Проверяет, что задачи возвращаются корректно для конкретного пользователя.

    Args:
        client (TestClient): Тестовый клиент для взаимодействия с API.
        created_user (dict): Данные пользователя.
        created_task (dict): Данные задачи.
    """
    user_id = created_user["id"]
    response = client.get(f"/tasks/user/{user_id}")
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) > 0
    assert json_response[0]["title"] == "Test Task"


def test_update_task(client, created_task):
    """Тестирование обновления задачи.

    Проверяет, что задача может быть успешно обновлена с новыми данными.

    Args:
        client (TestClient): Тестовый клиент для взаимодействия с API.
        created_task (dict): Данные задачи.
    """
    task_id = created_task["id"]
    update_data = {
        "title": "Updated Task",
        "description": "This task has been updated",
        "due_date": "2025-01-02"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert json_response["title"] == "Updated Task"
    assert json_response["description"] == "This task has been updated"
    assert json_response["due_date"] == "2025-01-02"


def test_delete_task(client, created_task):
    """Тестирование удаления задачи.

    Проверяет, что задача может быть успешно удалена.

    Args:
        client (TestClient): Тестовый клиент для взаимодействия с API.
        created_task (dict): Данные задачи.
    """
    task_id = created_task["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert json_response["id"] == task_id
