from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.events import IngressResponse, IngressSchema, RetrogradeResponse, RetrogradeSchema
from ...services.crossing_service import CrossingService
from ...services.events_service import EventsService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
crossing_service = CrossingService(ephemeris)
events_service = EventsService(ephemeris, crossing_service)


@router.get("/ingresses", response_model=IngressResponse, summary="Get sign ingresses for a planet")
async def get_ingresses(
    planet: Planet,
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    end_time: datetime | None = Query(None),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> IngressResponse:
    """
    Search for sign boundary crossings (0° sign entry) for a planet.
    """
    t_start = Time(start_time)
    count = 12 if end_time else 1

    events = events_service.get_sign_ingresses(
        t_start, planet, count=count, sidereal_mode=sidereal_mode
    )

    # Map domain PlanetaryEvent → IngressSchema
    ingresses = [
        IngressSchema(
            planet=e.planet.name,
            time=e.time,
            from_sign=e.from_sign or "",
            to_sign=e.to_sign or "",
        )
        for e in events
        if end_time is None or e.time <= end_time
    ]

    return IngressResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode), data=ingresses
    )


@router.get("/retrogrades", response_model=RetrogradeResponse, summary="Get planetary stations")
async def get_retrogrades(
    planet: Planet,
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    end_time: datetime | None = Query(None),
) -> RetrogradeResponse:
    """
    Search for planetary stations (turning Direct or Retrograde).
    """
    t_start = Time(start_time)

    if planet in [Planet.SUN, Planet.MOON]:
        return RetrogradeResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=[])

    events = events_service.get_retrograde_stations(t_start, planet, count=2)

    # Map domain PlanetaryEvent → RetrogradeSchema
    stations = [
        RetrogradeSchema(
            planet=e.planet.name,
            time=e.time,
            station_type=e.station_type or "UNKNOWN",
        )
        for e in events
        if end_time is None or e.time <= end_time
    ]

    return RetrogradeResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=stations)
