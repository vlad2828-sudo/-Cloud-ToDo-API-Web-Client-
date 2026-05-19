import os
from collections.abc import Generator

os.environ["DATABASE_URL"] = "sqlite:///./test_todo.db"
os.environ["API_KEY"] = "test-api-key"
os.environ["CORS_ALLOWED_ORIGINS"] = "http://testserver"

import pytest
from fastapi.testclient import TestClient

from app.db.models import Base
from app.db.session import engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def api_headers() -> dict[str, str]:
    return {"X-API-Key": "test-api-key"}
