from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from services.api.app.main import app


def test_healthcheck_returns_ok(monkeypatch) -> None:
    fake_cursor = MagicMock()
    fake_connection = MagicMock()
    fake_connection.cursor.return_value.__enter__.return_value = fake_cursor

    monkeypatch.setattr(
        "services.api.app.main.psycopg.connect",
        MagicMock(return_value=fake_connection),
    )

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    fake_cursor.execute.assert_called_once_with("SELECT 1")
