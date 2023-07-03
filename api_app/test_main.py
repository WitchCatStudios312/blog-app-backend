from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .database import Base
from .main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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


def test_create_post():
    response = client.post(
        "/posts/",
        json={"id": "0", "title": "title", "content": "content"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "title"
    assert data["content"] == "content"
    assert "id" in data
    post_id = data["id"]

    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "content"
    assert data["title"] == "title"
    assert data["id"] == post_id

def test_edit_post():
    response = client.put(
        "/posts/",
        json={"id": "1", "title": "test title", "content": "test content"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test title"
    assert data["content"] == "test content"
    assert data["id"] == 1

    response = client.get(f"/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test title"
    assert data["content"] == "test content"
    assert data["id"] == 1


def test_read_post():
    post_id = 1
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test title"
    assert data["content"] == "test content"
    assert data["id"] == post_id


def test_read_posts():
    client.post(
        "/posts/",
        json={"id": "2", "title": "second title", "content": "second content"},
    )
    client.post(
        "/posts/",
        json={"id": "0", "title": "third title", "content": "third content"},
    )

    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "test title"
    assert data[0]["content"] == "test content"
    assert data[0]["id"] == 1
    assert data[1]["title"] == "second title"
    assert data[1]["content"] == "second content"
    assert data[1]["id"] == 2
    assert data[2]["title"] == "third title"
    assert data[2]["content"] == "third content"
    assert data[2]["id"] == 3


def test_delete_post():
    client.delete("/posts/3")

    response = client.get("/posts/")
    assert response.status_code == 200
    assert response.is_success == True
    data = response.json()
    assert data[0]["title"] == "test title"
    assert data[0]["content"] == "test content"
    assert data[0]["id"] == 1
    assert data[1]["title"] == "second title"
    assert data[1]["content"] == "second content"
    assert data[1]["id"] == 2


def test_read_posts_no_data():
    client.delete("/posts/1")
    client.delete("/posts/2")
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert data == []

def test_read_post_no_data():
    post_id = 1
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Post not found"

def test_delete_post_no_data():
    response = client.delete("/posts/3")
    assert response.status_code == 404
    assert response.is_success == False
    data = response.json()
    assert data["detail"] == "Post not found"