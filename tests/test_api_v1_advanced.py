import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_financial_time_windows():
    response = client.get("/api/v1/financial/time-windows?max_days=30")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # Check that mandatory disclaimers exist in the top-level meta wrapper
    assert data["meta"].get("astro_data_only") is True
    assert data["meta"].get("no_financial_advice") is True
    
    assert "windows" in data["data"]
    # We may or may not have windows in a short 30 day span but it should be a list
    assert isinstance(data["data"]["windows"], list)


def test_signals_astro_intensity():
    response = client.get("/api/v1/signals/astro-intensity?max_days=1&step_hours=12")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "intensities" in data["data"]
    intensities = data["data"]["intensities"]
    assert len(intensities) > 0
    
    first = intensities[0]
    assert "score" in first
    assert "active_aspects_count" in first
    assert "top_contributors" in first


def test_signals_cluster_index():
    response = client.get("/api/v1/signals/cluster-index?max_days=1&step_hours=24&orb_degrees=20")
    assert response.status_code == 200
    data = response.json()
    
    # Ensure it returns an array of cluster index points
    assert "data" in data
    assert isinstance(data["data"], list)
    if len(data["data"]) > 0:
        first = data["data"][0]
        assert "stellar_density_score" in first
        assert "clusters" in first


def test_research_ephemeris_csv():
    # Only test a 1-day stream to not overload the unit testing environment
    response = client.get("/api/v1/research/ephemeris/csv?years=0.005&step_hours=24")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    
    content = response.text
    # Should at least contain headers and a few rows
    assert "Date(UTC),JulianDay,Planet,Longitude,Latitude,Distance,SpeedLong,IsRetrograde" in content
    assert "SUN" in content
    assert "MOON" in content
