from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base
from app.main import app, get_session
from app.models import MenuItem
from sqlalchemy.pool import StaticPool

def test_menu_returns_empty_list(monkeypatch) -> None:
    fake_connection = MagicMock()
    fake_connection.cursor.return_value.__enter__.return_value = MagicMock()
    fake_connect_cm = MagicMock()
    fake_connect_cm.__enter__.return_value = fake_connection
    monkeypatch.setattr(
        "app.main.psycopg.connect",
        MagicMock(return_value=fake_connect_cm),
    )

    engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool,)
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

