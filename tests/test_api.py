import pytest
from fastapi.testclient import TestClient
from ai_api.main import app
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model" in data

def test_get_empty_history():
    response = client.get("/conversation-history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_delete_nonexistent_user():
    response = client.delete("/conversation-history/nonexistent_user")
    assert response.status_code == 404
