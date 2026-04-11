from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.contexts import ZodiacType, build_western_chart_context
from app.core.constants import SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.main import app
from app.services.western import WesternProgressionService


client = TestClient(app)


def test_western_progression_service_uses_context_settings() -> None:
    context = build_western_chart_context(
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=True,
        capability="western.progression",
    )
    service = WesternProgressionService(context, ephemeris=Ephemeris())

    result = service.calculate_secondary_progression(
        Time(datetime(1990, 1, 1, 12, 0, tzinfo=UTC)),
        Time(datetime(2024, 1, 1, 12, 0, tzinfo=UTC)),
    )

    assert result.progression_date.year >= 1990
    assert len(result.planets) > 0


def test_western_progression_service_supports_tropical_context() -> None:
    context = build_western_chart_context(
        sidereal_mode=SiderealMode.LAHIRI,
        is_sidereal=False,
        capability="western.progression",
    )
    service = WesternProgressionService(context, ephemeris=Ephemeris())

    result = service.calculate_secondary_progression(
        Time(datetime(1990, 1, 1, 12, 0, tzinfo=UTC)),
        Time(datetime(2024, 1, 1, 12, 0, tzinfo=UTC)),
    )

    assert context.zodiac.zodiac == ZodiacType.TROPICAL
    assert len(result.planets) > 0


def test_v1_secondary_progression_route_runs_through_phase1_adapter() -> None:
    response = client.get(
        "/api/v1/progressions/secondary",
        params={
            "birth_time": "1990-01-01T12:00:00Z",
            "target_date": "2024-01-01T12:00:00Z",
            "sidereal_mode": 1,
            "is_sidereal": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["capability"] == "western.progression"
    assert payload["meta"]["feature_maturity"] == "beta"
    assert payload["meta"]["calculation_fingerprint"] is not None
    assert len(payload["data"]["planets"]) > 0
