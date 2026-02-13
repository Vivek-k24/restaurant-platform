from fastapi.testclient import TestClient

from services.api.app.main import app


def test_healthcheck_returns_ok(monkeypatch) -> None:
    monkeypatch.setenv("SKIP_DB_CHECK", "true")

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
