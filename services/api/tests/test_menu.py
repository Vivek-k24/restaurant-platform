from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from services.api.app.db import Base
from services.api.app.main import app, get_session
from services.api.app.models import MenuItem


def test_menu_returns_empty_list(monkeypatch) -> None:
    fake_connection = MagicMock()
    fake_connection.cursor.return_value.__enter__.return_value = MagicMock()
    monkeypatch.setattr(
        "services.api.app.main.psycopg.connect",
        MagicMock(return_value=fake_connection),
    )

    engine = create_engine("sqlite+pysqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_session():
        db: Session = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = override_get_session
    try:
        with TestClient(app) as client:
            response = client.get("/menu")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []

