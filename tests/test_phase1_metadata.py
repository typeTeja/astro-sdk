from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_natal_chart_response_includes_reproducibility_metadata() -> None:
    response = client.post(
        "/api/v1/charts/natal",
        json={
            "time": {"time": "2024-03-20T03:06:00Z"},
            "location": {"latitude": 51.5074, "longitude": -0.1278, "altitude": 0.0},
            "settings": {
                "house_system": "P",
                "sidereal_mode": 1,
                "is_sidereal": True,
                "heliocentric": False,
            },
        },
    )

    assert response.status_code == 200
    meta = response.json()["meta"]
    assert meta["capability"] == "western.chart"
    assert meta["feature_maturity"] == "beta"
    assert isinstance(meta["calculation_fingerprint"], str)
    assert len(meta["calculation_fingerprint"]) == 64
    assert meta["engine_version"] is not None


def test_natal_chart_fingerprint_is_deterministic_for_identical_inputs() -> None:
    payload = {
        "time": {"time": "2024-03-20T03:06:00Z"},
        "location": {"latitude": 51.5074, "longitude": -0.1278, "altitude": 0.0},
        "settings": {
            "house_system": "P",
            "sidereal_mode": 1,
            "is_sidereal": True,
            "heliocentric": False,
        },
    }

    first = client.post("/api/v1/charts/natal", json=payload)
    second = client.post("/api/v1/charts/natal", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert (
        first.json()["meta"]["calculation_fingerprint"]
        == second.json()["meta"]["calculation_fingerprint"]
    )


def test_transit_and_aspect_routes_include_capability_metadata() -> None:
    transit_response = client.post(
        "/api/v1/transits/scan",
        params={"transit_time": "2024-03-20T12:00:00Z", "aspect_types": "major"},
        json={
            "time": {"time": "1990-01-01T12:00:00Z"},
            "location": {"latitude": 40.7128, "longitude": -74.0060, "altitude": 0.0},
            "settings": {"sidereal_mode": 1, "is_sidereal": True},
        },
    )
    aspect_response = client.get(
        "/api/v1/aspects/calculate",
        params={
            "time": "2024-03-20T12:00:00Z",
            "sidereal_mode": 1,
            "aspect_types": "major",
        },
    )

    assert transit_response.status_code == 200
    assert transit_response.json()["meta"]["capability"] == "western.transit"
    assert transit_response.json()["meta"]["calculation_fingerprint"] is not None

    assert aspect_response.status_code == 200
    assert aspect_response.json()["meta"]["capability"] == "western.aspect"
    assert aspect_response.json()["meta"]["calculation_fingerprint"] is not None
