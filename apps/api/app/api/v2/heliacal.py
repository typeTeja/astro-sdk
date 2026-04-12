"""
/api/v2/heliacal — Heliacal risings/settings and planetary stations.
"""
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BeforeValidator

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet, validate_enum_by_name
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.heliacal import (
    HeliacalEventSchema,
    HeliacalResponse,
    StationSchema,
    StationsResponse,
)
from app.services.astronomy.visibility_service import AstronomyVisibilityService
from app.services.mundane.station_service import MundaneStationService

router = APIRouter()
ephemeris = Ephemeris()

# Standard 2.0 Planet Validator for Query Parameters

PlanetQuery = Annotated[Planet, BeforeValidator(lambda v: validate_enum_by_name(Planet, v))]


@router.get(
    "/rising",
    response_model=HeliacalResponse,
    summary="Find the next heliacal rising of a planet or star",
)
def get_heliacal_rising(
    planet: PlanetQuery,
    altitude: float = Query(0.0),
    time: datetime = Query(...),
    star_name: str = Query("", description="Star name for fixed stars (leave empty for planets)"),
    context: CalculationContext = Depends(get_calculation_context),
) -> HeliacalResponse:
    """
    Find the next heliacal rising — when a planet/star becomes visible again
    after its period of invisibility in the solar glare.
    """
    t = Time(time)
    visibility_service = AstronomyVisibilityService(context, ephemeris=ephemeris)

    result = visibility_service.calculate_heliacal_event(
        planet, t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
        (context.observer.altitude if context.observer else 0.0) or altitude,
        event_type=1, # Rising
        star_name=star_name
    )

    data = HeliacalEventSchema(
        planet=planet.name,
        event_type="HELIACAL_RISING",
        time=result.get("time"),
    )
    return HeliacalResponse(
        meta=get_meta(
            capability="astronomy.visibility.rising",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )


@router.get(
    "/setting",
    response_model=HeliacalResponse,
    summary="Find the next heliacal setting of a planet or star",
)
def get_heliacal_setting(
    planet: PlanetQuery,
    altitude: float = Query(0.0),
    time: datetime = Query(...),
    star_name: str = Query(""),
    context: CalculationContext = Depends(get_calculation_context),
) -> HeliacalResponse:
    """
    Find the next heliacal setting — when a planet/star disappears into the solar glare.
    """
    t = Time(time)
    visibility_service = AstronomyVisibilityService(context, ephemeris=ephemeris)

    result = visibility_service.calculate_heliacal_event(
        planet, t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
        (context.observer.altitude if context.observer else 0.0) or altitude,
        event_type=2, # Setting
        star_name=star_name
    )

    data = HeliacalEventSchema(
        planet=planet.name,
        event_type="HELIACAL_SETTING",
        time=result.get("time"),
    )
    return HeliacalResponse(
        meta=get_meta(
            capability="astronomy.visibility.setting",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )


@router.get(
    "/stations",
    response_model=StationsResponse,
    summary="Find all retrograde and direct stations for a planet in a year",
)
def get_stations(
    planet: PlanetQuery,
    year: int = Query(..., ge=1800, le=3000),
    context: CalculationContext = Depends(get_calculation_context),
) -> StationsResponse:
    """
    Find all station points (turning retrograde or direct) for a planet in a given year.
    """
    from datetime import datetime
    t_start = Time(datetime(year, 1, 1))
    t_end = Time(datetime(year, 12, 31, 23, 59, 59))

    station_service = MundaneStationService(context, ephemeris=ephemeris)
    events = station_service.scan_stations(planet, t_start, t_end)

    data = [
        StationSchema(
            time=e.time,
            station_type=e.station_type,
            julian_day=Time(e.time).julian_day,
        )
        for e in events
    ]
    return StationsResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="mundane.stations"
        ),
        data=data
    )
