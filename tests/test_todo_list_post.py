from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.models.models import TodoList, TodoItem

SQLALCHEMY_DATABASE_URL = os.getenv('TEST_DATABASE_URL')


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_todo_list():
    response = client.post("/todo/list/", json={"name": "Test List", "items": [{"title": "Test Item"}]})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test List"
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Test Item"
