import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.ephemeris import Ephemeris

@pytest.fixture(scope="session")
def client():
    """
    Global FastAPI test client.
    Using context manager to trigger startup events (database creation).
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def ephemeris():
    """
    Singleton Swiss Ephemeris instance.
    """
    return Ephemeris()
