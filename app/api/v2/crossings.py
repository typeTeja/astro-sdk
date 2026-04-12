from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.crossings import (
    AspectCrossingResponse,
    AspectCrossingSchema,
    PlanetaryReturnResponse,
    PlanetaryReturnSchema,
)
from app.services.astronomy.crossing_service import AstronomyCrossingService
from app.services.western.return_service import WesternReturnService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/return",
    response_model=PlanetaryReturnResponse,
    summary="Find the next planetary return to a given longitude",
)
def get_planetary_return(
    planet: Planet,
    target_longitude: float = Query(..., ge=0.0, lt=360.0, description="Target longitude in degrees"),
    start_time: datetime = Query(...),
    max_days: float = Query(400.0, gt=0, le=36525.0),
    context: CalculationContext = Depends(get_calculation_context),
) -> PlanetaryReturnResponse:
    """
    Find the next time a planet returns to a specific ecliptic longitude.
    Useful for solar returns, lunar returns, and planetary returns.
    """
    t_start = Time(start_time)
    return_service = WesternReturnService(context, ephemeris=ephemeris)
    result = return_service.find_planetary_return(
        planet,
        target_longitude,
        t_start,
        max_days=max_days,
    )

    # Use native context fingerprint
    data = PlanetaryReturnSchema(
        planet=planet.name,
        return_time=result.dt,
        longitude=target_longitude,
    )
    return PlanetaryReturnResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="western.return",
        ),
        data=[data],
    )


@router.get(
    "/aspect",
    response_model=AspectCrossingResponse,
    summary="Find exact inter-planetary aspect crossing",
)
def get_aspect_crossing(
    p1: Planet,
    p2: Planet,
    target_angle: float = Query(0.0, ge=0.0, le=180.0, description="Aspect angle (0=conjunction, 180=opposition)"),
    start_time: datetime = Query(...),
    max_days: float = Query(1000.0, gt=0, le=36525.0),
    context: CalculationContext = Depends(get_calculation_context),
) -> AspectCrossingResponse:
    """
    Find the exact moment two planets achieve a specific angular separation.
    """
    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + max_days)

    crossing_service = AstronomyCrossingService(context, ephemeris=ephemeris)

    crossings = crossing_service.find_aspect_crossings(p1, p2, target_angle, t_start, t_end)

    data = [
        AspectCrossingSchema(
            p1=p1.name,
            p2=p2.name,
            target_angle=target_angle,
            crossing_time=c.dt,
        )
        for c in crossings
    ]
    return AspectCrossingResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="astronomy.crossings.aspect"
        ),
        data=data
    )
