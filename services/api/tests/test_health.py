from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app


def test_healthcheck_returns_ok(monkeypatch) -> None:
    # Fake cursor
    fake_cursor = MagicMock()

    # Fake connection that returns fake_cursor in context manager
    fake_connection = MagicMock()
    fake_connection.cursor.return_value.__enter__.return_value = fake_cursor

    # psycopg.connect() must return a context manager
    fake_connect_cm = MagicMock()
    fake_connect_cm.__enter__.return_value = fake_connection

    # Patch psycopg.connect
    monkeypatch.setattr(
        "app.main.psycopg.connect",
        MagicMock(return_value=fake_connect_cm),
    )

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    fake_cursor.execute.assert_called_once_with("SELECT 1")
