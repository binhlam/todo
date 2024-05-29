import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import text

from ..database import get_db
from ..main import app
from ..models.todo import Todo
from ..services.security.auth import get_current_user
from .utils import (TestSessionLocal, engine, init_user,
                    override_get_current_user, override_get_db)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)
db = TestSessionLocal()

def cleanup():
  with engine.connect() as conn:
      conn.execute(text("DELETE FROM todos;"))
      conn.execute(text("truncate users restart identity cascade;"))
      conn.commit()

@pytest.fixture
def test_create():
  user = init_user()
  yield user
  cleanup()


@pytest.fixture
def test_read():
  init_user()
  todo = Todo(
    title="test",
    description="test",
    priority=5,
    complete=0,
    owner_id=1
  )
  db.add(todo)
  db.commit()
  yield todo
  cleanup()

def test_read_all_authenticated(test_read):
  response = client.get("/api/v1/todos")
  assert response.status_code == status.HTTP_200_OK
  assert response.json()[0]['title'] == 'test'
  assert response.json()[0]['description'] == 'test'
  assert response.json()[0]['priority'] == 5
  assert response.json()[0]['complete'] == 0
  assert response.json()[0]['owner_id'] == 1

def test_read_by_id_authenticated(test_read):
  response = client.get("/api/v1/todos/1")
  assert response.status_code == status.HTTP_200_OK
  assert response.json()['title'] == 'test'
  assert response.json()['description'] == 'test'
  assert response.json()['priority'] == 5
  assert response.json()['complete'] == 0
  assert response.json()['owner_id'] == 1

def test_update_authenticated(test_read):
  request_data = {
    'title': 'update',
    'description': 'test update',
    'priority': 5,
    'complete': 0
  }
  response = client.put("/api/v1/todos/1", json=request_data)
  assert response.status_code == status.HTTP_204_NO_CONTENT

def test_create_authenticated(test_create):
  request_data = {
    'title': 'create',
    'description': 'test create',
    'priority': 5,
    'complete': 0
  }
  response = client.post("/api/v1/todos", json=request_data)
  assert response.status_code == status.HTTP_201_CREATED

def test_delete_authenticated(test_read):
  response = client.delete("/api/v1/todos/1")
  assert response.status_code == status.HTTP_204_NO_CONTENT
