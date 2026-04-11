from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.events import IngressResponse, IngressSchema, RetrogradeResponse, RetrogradeSchema
from ...services.mundane.ingress_service import IngressService
from ...services.mundane.station_service import StationService
from ...contexts.factories import create_default_context
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


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
    t_end = Time(end_time) if end_time else Time(start_time + timedelta(days=365))
    
    context = create_default_context()
    context.zodiac.sidereal_mode = sidereal_mode
    context.zodiac.zodiac = "sidereal"
    
    ingress_service = IngressService(context, ephemeris=ephemeris)
    events = ingress_service.scan_ingresses(planet, t_start, t_end)

    # Map domain MundaneIngress → IngressSchema
    ingresses = [
        IngressSchema(
            planet=e.planet.name,
            time=e.time,
            from_sign=str(e.sign_from),
            to_sign=str(e.sign_to),
        )
        for e in events
    ]

    return IngressResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode), data=ingresses
    )

from datetime import timedelta

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
    t_end = Time(end_time) if end_time else Time(start_time + timedelta(days=365))

    if planet in [Planet.SUN, Planet.MOON]:
        return RetrogradeResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=[])

    context = create_default_context()
    station_service = StationService(context, ephemeris=ephemeris)
    events = station_service.scan_stations(planet, t_start, t_end)

    # Map domain StationEvent → RetrogradeSchema
    stations = [
        RetrogradeSchema(
            planet=e.planet.name,
            time=e.time,
            station_type=e.station_type,
        )
        for e in events
    ]

    return RetrogradeResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=stations)
