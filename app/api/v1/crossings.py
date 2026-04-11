"""
/api/v1/crossings — Planetary returns and exact-angle crossings.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.time import Time
from ...schemas.crossings import AspectCrossingResponse, AspectCrossingSchema, PlanetaryReturnResponse, PlanetaryReturnSchema
from ...services.mundane.crossing_service import CrossingService
from ...services.western.return_service import WesternReturnService
from ...contexts.factories import create_default_context
from ..common import build_western_chart_context, calculation_metadata
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/return",
    response_model=PlanetaryReturnResponse,
    summary="Find the next planetary return to a given longitude",
)
async def get_planetary_return(
    planet: Planet,
    target_longitude: float = Query(..., ge=0.0, lt=360.0, description="Target longitude in degrees"),
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
    max_days: float = Query(400.0, gt=0, le=36525.0),
) -> PlanetaryReturnResponse:
    """
    Find the next time a planet returns to a specific ecliptic longitude.
    Useful for solar returns, lunar returns, and planetary returns.
    """
    t_start = Time(start_time)
    context = create_default_context()
    context.zodiac.sidereal_mode = sidereal_mode
    context.zodiac.is_sidereal = True
    
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
            is_sidereal=True,
            sidereal_mode=sidereal_mode,
            capability="western.return",
            calculation_fingerprint=context.fingerprint,
        ),
        data=[data],
    )


@router.get(
    "/aspect",
    response_model=AspectCrossingResponse,
    summary="Find exact inter-planetary aspect crossing",
)
async def get_aspect_crossing(
    p1: Planet,
    p2: Planet,
    target_angle: float = Query(0.0, ge=0.0, le=180.0, description="Aspect angle (0=conjunction, 180=opposition)"),
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    max_days: float = Query(1000.0, gt=0, le=36525.0),
) -> AspectCrossingResponse:
    """
    Find the exact moment two planets achieve a specific angular separation.
    """
    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + max_days)
    
    context = create_default_context()
    crossing_service = CrossingService(context, ephemeris=ephemeris)

    crossings = crossing_service.find_aspects(p1, p2, target_angle, t_start, t_end)

    data = [
        AspectCrossingSchema(
            p1=p1.name,
            p2=p2.name,
            target_angle=target_angle,
            crossing_time=c.time,
        )
        for c in crossings
    ]
    return AspectCrossingResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)
