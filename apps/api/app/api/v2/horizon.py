"""
/api/v2/horizon — Rise, set, transit, and twilight times.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.horizon import RiseSetResponse, RiseSetSchema, TwilightResponse, TwilightSchema
from app.services.astronomy.horizon_service import AstronomyHorizonService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/rise-set",
    response_model=RiseSetResponse,
    summary="Calculate rise, transit, and set times for a planet",
)
def get_rise_set(
    planet: Planet,
    altitude: float = Query(0.0, description="Observer altitude in metres"),
    time: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> RiseSetResponse:
    """
    Calculate when a planet rises, culminates (transits the meridian), and sets
    at a given geographic location.
    """
    t = Time(time)
    horizon_service = AstronomyHorizonService(context, ephemeris=ephemeris)

    rise_time = horizon_service.get_horizon_event(
        planet, t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
        (context.observer.altitude if context.observer else 0.0) or altitude,
        is_rise=True
    )
    set_time = horizon_service.get_horizon_event(
        planet, t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
        (context.observer.altitude if context.observer else 0.0) or altitude,
        is_rise=False
    )
    transit_time = horizon_service.get_transit(
        planet, t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
        (context.observer.altitude if context.observer else 0.0) or altitude
    )

    data = RiseSetSchema(
        planet=planet.name,
        rise=rise_time.dt if rise_time else None,
        transit=transit_time.dt if transit_time else None,
        set=set_time.dt if set_time else None,
    )
    return RiseSetResponse(
        meta=get_meta(
            capability="astronomy.horizon.rise_set",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )


@router.get(
    "/twilight",
    response_model=TwilightResponse,
    summary="Calculate civil, nautical, or astronomical twilight",
)
def get_twilight(
    altitude: float = Query(0.0),
    time: datetime = Query(...),
    twilight_type: str = Query("civil", description="civil | nautical | astronomical"),
    context: CalculationContext = Depends(get_calculation_context),
) -> TwilightResponse:
    """
    Calculate dawn and dusk for a given twilight type.
    """
    t = Time(time)
    horizon_service = AstronomyHorizonService(context, ephemeris=ephemeris)
    result = horizon_service.get_twilight(
        t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
        (context.observer.altitude if context.observer else 0.0) or altitude,
        twilight_type
    )

    dawn = result["dawn"]
    dusk = result["dusk"]

    data = TwilightSchema(
        twilight_type=twilight_type,
        dawn=dawn.dt if dawn else None,
        dusk=dusk.dt if dusk else None,
    )
    return TwilightResponse(
        meta=get_meta(
            capability="astronomy.horizon.twilight",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )
