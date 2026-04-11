from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.contexts import CoordinateSystem, ZodiacType
from app.contexts import build_western_chart_context
from app.core.constants import HouseSystem, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.engine.chart_engine import ChartEngine
from app.main import app
from app.services.western import WesternChartService


client = TestClient(app)


def test_western_chart_context_builder_maps_legacy_settings() -> None:
    context = build_western_chart_context(
        house_system=HouseSystem.WHOLE_SIGN,
        sidereal_mode=SiderealMode.KRISHNAMURTI,
        is_sidereal=True,
        heliocentric=True,
        latitude=12.97,
        longitude=77.59,
        altitude=920.0,
    )

    assert context.zodiac.zodiac == ZodiacType.SIDEREAL
    assert context.zodiac.sidereal_mode == SiderealMode.KRISHNAMURTI
    assert context.coordinate.system == CoordinateSystem.HELIOCENTRIC
    assert context.house.system == HouseSystem.WHOLE_SIGN
    assert context.observer is not None


def test_western_chart_service_creates_chart_from_context() -> None:
    context = build_western_chart_context(
        house_system=HouseSystem.PLACIDUS,
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=True,
        heliocentric=False,
        latitude=51.5074,
        longitude=-0.1278,
    )
    service = WesternChartService(context, ephemeris=Ephemeris())

    chart = service.create_chart(Time(datetime(2024, 3, 20, 3, 6, tzinfo=UTC)), 51.5074, -0.1278)

    assert chart.metadata["capability"] == "western.chart"
    assert chart.metadata["maturity"] == "beta"
    assert len(chart.planets) > 0
    assert chart.houses is not None


def test_v1_natal_chart_route_runs_through_phase0_adapter_path() -> None:
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
    payload = response.json()
    assert payload["meta"]["zodiac"] == "sidereal"
    assert len(payload["data"]["planets"]) > 0


def test_chart_engine_now_delegates_through_phase0_context_service() -> None:
    engine = ChartEngine()

    chart = engine.create_chart(
        Time(datetime(2024, 3, 20, 3, 6, tzinfo=UTC)),
        lat=51.5074,
        lon=-0.1278,
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=True,
        heliocentric=False,
    )

    assert chart.metadata["capability"] == "western.chart"
    assert chart.metadata["maturity"] == "beta"
    assert len(chart.planets) > 0
