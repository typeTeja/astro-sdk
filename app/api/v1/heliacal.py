"""
/api/v1/heliacal — Heliacal risings/settings and planetary stations.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import Planet
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.heliacal import HeliacalResponse, HeliacalEventSchema, StationsResponse, StationSchema
from ...services.heliacal_service import HeliacalService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
heliacal_service = HeliacalService(ephemeris)


@router.get(
    "/rising",
    response_model=HeliacalResponse,
    summary="Find the next heliacal rising of a planet or star",
)
async def get_heliacal_rising(
    planet: Planet,
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    altitude: float = Query(0.0),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    star_name: str = Query("", description="Star name for fixed stars (leave empty for planets)"),
) -> HeliacalResponse:
    """
    Find the next heliacal rising — when a planet/star becomes visible again
    after its period of invisibility in the solar glare.
    """
    t = Time(time)
    result = heliacal_service.calculate_heliacal_rising(
        planet, t, latitude, longitude, altitude, star_name
    )

    data = HeliacalEventSchema(
        planet=planet.name,
        event_type="HELIACAL_RISING",
        time=result.dt if result else None,
    )
    return HeliacalResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)


@router.get(
    "/setting",
    response_model=HeliacalResponse,
    summary="Find the next heliacal setting of a planet or star",
)
async def get_heliacal_setting(
    planet: Planet,
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    altitude: float = Query(0.0),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    star_name: str = Query(""),
) -> HeliacalResponse:
    """
    Find the next heliacal setting — when a planet/star disappears into the solar glare.
    """
    t = Time(time)
    result = heliacal_service.calculate_heliacal_setting(
        planet, t, latitude, longitude, altitude, star_name
    )

    data = HeliacalEventSchema(
        planet=planet.name,
        event_type="HELIACAL_SETTING",
        time=result.dt if result else None,
    )
    return HeliacalResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)


@router.get(
    "/stations",
    response_model=StationsResponse,
    summary="Find all retrograde and direct stations for a planet in a year",
)
async def get_stations(
    planet: Planet,
    year: int = Query(..., ge=1800, le=3000),
) -> StationsResponse:
    """
    Find all station points (turning retrograde or direct) for a planet in a given year.
    """
    raw = heliacal_service.find_all_stations(planet, year)

    data = [
        StationSchema(
            time=s["time"].dt,
            station_type=s["type"],
            julian_day=s["jd"],
        )
        for s in raw
    ]
    return StationsResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)
