# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AMC Information Chatbot API"}

def test_get_topics():
    response = client.get("/topics")
    assert response.status_code == 200
    assert "topics" in response.json()
