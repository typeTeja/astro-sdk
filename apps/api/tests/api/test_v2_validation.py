import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_topocentric_without_coordinates_returns_400():
    """
    Verify that requesting topocentric coordinate system without latitude/longitude
    returns a 400 Bad Request (Strict Validation rule).
    """
    params = {
        "coordinate_system": "topocentric",
        "planet": "sun",
        "time": "2024-01-01T12:00:00Z"
    }
    response = client.get("/api/v2/astronomy/planet-position", params=params)
    
    assert response.status_code == 400
    assert "Topocentric calculations require explicit latitude and longitude" in response.json()["detail"]

def test_topocentric_with_coordinates_returns_200():
    """
    Verify that topocentric works when coordinates are provided.
    """
    params = {
        "coordinate_system": "topocentric",
        "planet": "sun",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "time": "2024-01-01T12:00:00Z"
    }
    response = client.get("/api/v2/astronomy/planet-position", params=params)
    assert response.status_code == 200

def test_geocentric_without_coordinates_returns_200():
    """
    Verify that geocentric remains the default and doesn't require coordinates.
    """
    params = {
        "planet": "sun",
        "time": "2024-01-01T12:00:00Z"
    }
    response = client.get("/api/v2/astronomy/planet-position", params=params)
    assert response.status_code == 200
