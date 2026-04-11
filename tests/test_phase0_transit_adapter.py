from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.contexts import CoordinateSystem, ZodiacType, build_western_chart_context
from app.core.constants import SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.engine.chart_engine import ChartEngine
from app.main import app
from app.services.western import WesternTransitService


client = TestClient(app)


def test_transit_context_builder_supports_transit_capability() -> None:
    context = build_western_chart_context(
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=True,
        heliocentric=False,
        latitude=40.7128,
        longitude=-74.0060,
        capability="western.transit",
    )

    assert context.feature.capability == "western.transit"
    assert context.zodiac.zodiac == ZodiacType.SIDEREAL
    assert context.coordinate.system == CoordinateSystem.GEOCENTRIC


def test_western_transit_service_scans_against_chart_domain_positions() -> None:
    engine = ChartEngine()
    natal_chart = engine.create_chart(
        Time(datetime(1990, 1, 1, 12, 0, tzinfo=UTC)),
        lat=40.7128,
        lon=-74.0060,
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=True,
        heliocentric=False,
    )
    context = build_western_chart_context(
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=True,
        heliocentric=False,
        latitude=40.7128,
        longitude=-74.0060,
        capability="western.transit",
    )
    service = WesternTransitService(context, ephemeris=Ephemeris())

    aspects = service.scan_transits(
        natal_chart.planets,
        Time(datetime(2024, 3, 20, 12, 0, tzinfo=UTC)),
        aspect_types=["major"],
    )

    assert isinstance(aspects, list)


def test_v1_transit_scan_route_runs_through_phase0_transit_adapter() -> None:
    response = client.post(
        "/api/v1/transits/scan",
        params={"transit_time": "2024-03-20T12:00:00Z", "aspect_types": "major"},
        json={
            "time": {"time": "1990-01-01T12:00:00Z"},
            "location": {"latitude": 40.7128, "longitude": -74.0060, "altitude": 0.0},
            "settings": {"sidereal_mode": 1, "is_sidereal": True},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["zodiac"] == "sidereal"
    assert "aspects" in payload["data"]
