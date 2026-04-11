from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.contexts import build_western_chart_context
from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.main import app
from app.services.western import WesternReturnService


client = TestClient(app)


def test_western_return_service_uses_context_backed_planetary_return() -> None:
    context = build_western_chart_context(
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=True,
        capability="western.return",
    )
    service = WesternReturnService(context, ephemeris=Ephemeris())

    result = service.find_planetary_return(
        Planet.SUN,
        0.0,
        Time(datetime(2024, 3, 19, 0, 0, tzinfo=UTC)),
        max_days=30.0,
    )

    assert result.dt.year == 2024


def test_v1_planetary_return_route_runs_through_phase1_adapter() -> None:
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
    assert payload["meta"]["capability"] == "western.return"
    assert payload["meta"]["feature_maturity"] == "beta"
    assert payload["meta"]["calculation_fingerprint"] is not None
    assert payload["data"][0]["planet"] == "SUN"
