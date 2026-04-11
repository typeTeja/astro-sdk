from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.contexts import build_western_chart_context
from app.core.constants import SiderealMode
from app.core.time import Time
from app.engine.chart_engine import ChartEngine
from app.main import app
from app.services.western import WesternAspectService


client = TestClient(app)


def test_western_aspect_service_calculates_aspects_from_chart_positions() -> None:
    engine = ChartEngine()
    chart = engine.create_chart(
        Time(datetime(2024, 3, 20, 12, 0, tzinfo=UTC)),
        lat=0.0,
        lon=0.0,
        sidereal_mode=SiderealMode.LAHIRI,
    )
    context = build_western_chart_context(
        sidereal_mode=SiderealMode.LAHIRI,
        capability="western.aspect",
    )
    service = WesternAspectService(context)

    matches = service.calculate_aspects(chart.planets, aspect_types=["major"])

    assert isinstance(matches, list)


def test_v1_aspects_route_runs_through_phase0_aspect_adapter() -> None:
    response = client.get(
        "/api/v1/aspects/calculate",
        params={
            "time": "2024-03-20T12:00:00Z",
            "sidereal_mode": 1,
            "aspect_types": "major",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["zodiac"] == "sidereal"
    assert "aspects" in payload["data"]
