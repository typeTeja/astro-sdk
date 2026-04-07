from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.astro import PlanetPositionData
from ...schemas.transits import SecondaryProgressionData, SecondaryProgressionResponse
from ...services.progression_service import ProgressionService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
progression_service = ProgressionService(ephemeris)


@router.get(
    "/secondary",
    response_model=SecondaryProgressionResponse,
    summary="Get secondary progression positions",
)
async def get_secondary_progression(
    birth_time: datetime = Query(...),
    target_date: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> SecondaryProgressionResponse:
    """
    Calculate Secondary Progressions (Day-for-a-Year) for a given life moment.
    """
    t_birth = Time(birth_time)
    t_target = Time(target_date)

    # 1. Calculate progressions → returns ProgressedChart domain object
    prog = progression_service.calculate_secondary_progression(
        t_birth, t_target, sidereal_mode=sidereal_mode
    )

    # 2. Map domain dict records → PlanetPositionData schemas (schema layer)
    planets_data = [
        PlanetPositionData(
            planet=str(p["planet"]),
            longitude=float(p["longitude"]),  # type: ignore[arg-type]
            latitude=float(p["latitude"]),  # type: ignore[arg-type]
            distance=float(p["distance"]),  # type: ignore[arg-type]
            speed_long=float(p["speed_long"]),  # type: ignore[arg-type]
            is_retrograde=bool(p["is_retrograde"]),
            sign=int(p["sign"]),  # type: ignore[arg-type]
            sign_name=str(p["sign_name"]),
        )
        for p in prog.planets
    ]

    data = SecondaryProgressionData(
        progression_date=prog.progression_date,
        planets=planets_data,
    )

    return SecondaryProgressionResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode), data=data
    )
