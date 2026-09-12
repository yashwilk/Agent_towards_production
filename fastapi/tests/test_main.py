"""Unit tests for the FastAPI agent service."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_endpoint():
    response = client.post("/agent", json={"query": "Test query"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert "Agent" in response.json()["response"]


def test_stream_endpoint():
    with client.stream("POST", "/agent/stream", json={"query": "Test query"}) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        content = "".join(response.iter_text())
        assert 'data: {"token":' in content


def test_agent_endpoint_rejects_wrong_api_key(monkeypatch):
    monkeypatch.setattr("config.API_KEY", "secret")
    response = client.post("/agent", json={"query": "Test query"}, headers={"X-API-Key": "wrong"})
    assert response.status_code == 403


def test_agent_endpoint_requires_api_key_when_configured(monkeypatch):
    monkeypatch.setattr("config.API_KEY", "secret")
    response = client.post("/agent", json={"query": "Test query"})
    assert response.status_code == 401
