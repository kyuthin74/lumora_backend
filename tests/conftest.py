"""Test configuration and fixtures.

All external dependencies are isolated: in-memory SQLite instead of the real
database, a fake Gemini chat, no SMTP and no push-notification scheduler.
"""

import os

# Must be set before app modules import settings.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ["PUSH_REMINDER_ENABLED"] = "false"

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.utils.security import create_access_token, get_password_hash


# Models use PostgreSQL-only column types; let SQLite create them as JSON for tests.
from sqlalchemy.types import ARRAY
from sqlalchemy.ext.compiler import compiles


@compiles(ARRAY, "sqlite")
def _compile_array_for_sqlite(type_, compiler, **kw):
    return "JSON"


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # one shared connection (WebSocket runs in another thread)
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Fresh in-memory database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class FakeChat:
    """Stands in for a Gemini chat session."""

    def __init__(self):
        self.sent = []

    def send_message(self, text):
        self.sent.append(text)

        class _Response:
            pass

        r = _Response()
        r.text = "I'm here for you."
        return r

    def get_history(self):
        return []


@pytest.fixture(scope="function")
def client(db_session, monkeypatch):
    """TestClient wired to the test DB with external services mocked."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # The WebSocket endpoint calls next(get_db()) directly, so patch it too.
    monkeypatch.setattr("app.api.chatbot.get_db", override_get_db)
    # Fake Gemini (no API key / network needed).
    monkeypatch.setattr("app.api.chatbot.init_gemini_chat", lambda history=None: FakeChat())
    # No SMTP during signup.
    async def _no_email(*args, **kwargs):
        return None
    monkeypatch.setattr("app.api.auth.send_welcome_email", _no_email)
    # No background scheduler.
    monkeypatch.setattr("app.main.start_push_reminder_scheduler", lambda: None)
    monkeypatch.setattr("app.main.stop_push_reminder_scheduler", lambda: None)
    # Reset one-connection-per-user registry between tests.
    from app.api import chatbot
    chatbot.active_connections.clear()

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    user = User(
        email="testuser@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123"),
        is_notify_enabled=False,
        is_risk_alert_enabled=False,
        is_push_reminder_enabled=False,
        created_at=datetime.utcnow(),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_token(test_user):
    return create_access_token(data={"sub": str(test_user.id), "email": test_user.email})
