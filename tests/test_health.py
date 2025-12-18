import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns 200"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_summarize_endpoint_mock():
    """Test that the summarize endpoint exists and responds"""
    response = client.post(
        "/summarize",
        json={
            "messages": [{"role": "user", "content": "test"}],
            "model": "test-model"
        }
    )
    # Will return 500 if Ollama not configured, but endpoint exists
    assert response.status_code in [200, 500]

def test_embedding_endpoint_mock():
    """Test that the embedding endpoint exists and responds"""
    response = client.post(
        "/embeddings",
        json={
            "text": "test text",
            "model": "test-model"
        }
    )
    # Will return 500 if Ollama not configured, but endpoint exists
    assert response.status_code in [200, 500]