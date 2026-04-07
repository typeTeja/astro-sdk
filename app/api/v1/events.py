from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.events import IngressResponse, RetrogradeResponse
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

    # Calculate count based on start/end or use default
    # If end_time provided, enough to cover a year (12)
    count = 12 if end_time else 1

    ingresses = events_service.get_sign_ingresses(
        t_start, planet, count=count, sidereal_mode=sidereal_mode
    )

    # Filtering if end_time provided
    if end_time:
        ingresses = [ing for ing in ingresses if ing.time <= end_time]

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

    # Sun and Moon don't go retrograde
    if planet in [Planet.SUN, Planet.MOON]:
        return RetrogradeResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=[])

    # Use a default count of 2 to catch the next Rx and Dir periods
    stations = events_service.get_retrograde_stations(t_start, planet, count=2)

    # Filtering if end_time provided
    if end_time:
        stations = [st for st in stations if st.time <= end_time]

    return RetrogradeResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=stations)
