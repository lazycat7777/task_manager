import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def create_user():
    """Создаёт пользователя для тестов."""
    user_data = {"username": "testuser", "email": "test@example.com"}
    response = client.post("/users/", json=user_data)
    return response.json()

def test_create_user():
    """Тестирует создание нового пользователя через API."""
    user_data = {"username": "testuser", "email": "test@example.com"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201 
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"  

def test_read_user(create_user):
    """Тестирует получение информации о пользователе по его ID."""
    user_id = create_user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_create_task(create_user):
    """Тестирует создание новой задачи для пользователя через API."""
    task_data = {"title": "Test Task", "description": "Test Description", "due_date": "2025-01-01", "user_id": create_user["id"]}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201 
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "Test Description"
    assert response.json()["due_date"] == "2025-01-01"  
    assert response.json()["user_id"] == create_user["id"]

def test_read_tasks(create_user):
    """Тестирует получение всех задач пользователя по его ID."""
    task_data = {"title": "Test Task", "description": "Test Description", "due_date": "2025-01-01", "user_id": create_user["id"]}
    client.post("/tasks/", json=task_data)
    response = client.get(f"/tasks/user/{create_user['id']}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Task"
    assert response.json()[0]["description"] == "Test Description"

def test_update_task(create_user):
    """Тестирует обновление задачи по её ID."""
    task_data = {"title": "Test Task", "description": "Test Description", "due_date": "2025-01-01", "user_id": create_user["id"]}
    task_response = client.post("/tasks/", json=task_data)
    task_id = task_response.json()["id"]
    update_data = {"title": "Updated Task", "description": "Updated Description", "due_date": "2025-02-01", "user_id": create_user["id"]}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "Updated Description"
    assert response.json()["due_date"] == "2025-02-01"

def test_delete_task(create_user):
    """Тестирует удаление задачи по её ID."""
    task_data = {"title": "Test Task", "description": "Test Description", "due_date": "2025-01-01", "user_id": create_user["id"]}
    task_response = client.post("/tasks/", json=task_data)
    task_id = task_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
