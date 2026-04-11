"""
/api/v1/horizon — Rise, set, transit, and twilight times.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import Planet
from ...core.time import Time
from ...schemas.horizon import RiseSetResponse, RiseSetSchema, TwilightResponse, TwilightSchema
from ...services.astronomy.horizon_service import AstronomyHorizonService
from ...contexts.factories import create_default_context
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/rise-set",
    response_model=RiseSetResponse,
    summary="Calculate rise, transit, and set times for a planet",
)
async def get_rise_set(
    planet: Planet,
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    altitude: float = Query(0.0, description="Observer altitude in metres"),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> RiseSetResponse:
    """
    Calculate when a planet rises, culminates (transits the meridian), and sets
    at a given geographic location.
    """
    t = Time(time)
    context = create_default_context()
    horizon_service = AstronomyHorizonService(context, ephemeris=ephemeris)

    rise_time = horizon_service.get_horizon_event(planet, t, latitude, longitude, altitude, is_rise=True)
    set_time = horizon_service.get_horizon_event(planet, t, latitude, longitude, altitude, is_rise=False)
    transit_time = horizon_service.get_transit(planet, t, latitude, longitude, altitude)

    data = RiseSetSchema(
        planet=planet.name,
        rise=rise_time.dt if rise_time else None,
        transit=transit_time.dt if transit_time else None,
        set=set_time.dt if set_time else None,
    )
    return RiseSetResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)


@router.get(
    "/twilight",
    response_model=TwilightResponse,
    summary="Calculate civil, nautical, or astronomical twilight",
)
async def get_twilight(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    altitude: float = Query(0.0),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    twilight_type: str = Query("civil", description="civil | nautical | astronomical"),
) -> TwilightResponse:
    """
    Calculate dawn and dusk for a given twilight type.
    """
    t = Time(time)
    context = create_default_context()
    horizon_service = AstronomyHorizonService(context, ephemeris=ephemeris)
    result = horizon_service.get_twilight(t, latitude, longitude, altitude, twilight_type)

    dawn = result["dawn"]
    dusk = result["dusk"]

    data = TwilightSchema(
        twilight_type=twilight_type,
        dawn=dawn.dt if dawn else None,
        dusk=dusk.dt if dusk else None,
    )
    return TwilightResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)
