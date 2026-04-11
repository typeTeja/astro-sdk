from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.main import app
from app.services.natal_service import NatalService


client = TestClient(app)


def test_natal_service_uses_tropical_when_sidereal_mode_is_none() -> None:
    service = NatalService(Ephemeris())
    time = Time(datetime(2024, 3, 20, 3, 6, tzinfo=UTC))

    positions = service.calculate_positions(time, sidereal_mode=None)
    sun = next(p for p in positions if p.planet == Planet.SUN)

    assert sun.longitude < 1.0 or sun.longitude > 359.0


def test_crossings_return_endpoint_honors_query_contract() -> None:
    response = client.get(
        "/api/v1/crossings/return",
        params={
            "planet": 0,
            "target_longitude": 0.0,
            "start_time": "2024-03-19T00:00:00Z",
            "sidereal_mode": 1,
            "max_days": 30,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"][0]["planet"] == "SUN"
    assert payload["data"][0]["longitude"] == 0.0


def test_helion_transits_endpoint_returns_success() -> None:
    response = client.post(
        "/api/v1/transits/helion",
        params={"transit_time": "2024-03-20T12:00:00Z"},
        json={
            "time": {"time": "2000-01-01T12:00:00Z"},
            "location": {"latitude": 0.0, "longitude": 0.0, "altitude": 0.0},
            "settings": {},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["coordinate_system"] == "heliocentric"
    assert "aspects" in payload["data"]


def test_declination_transits_endpoint_is_explicitly_not_implemented() -> None:
    response = client.post(
        "/api/v1/transits/declination",
        params={"transit_time": "2024-03-20T12:00:00Z"},
        json={
            "time": {"time": "2000-01-01T12:00:00Z"},
            "location": {"latitude": 0.0, "longitude": 0.0, "altitude": 0.0},
            "settings": {},
        },
    )

    assert response.status_code == 501
