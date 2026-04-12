from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.events import IngressResponse, IngressSchema, RetrogradeResponse, RetrogradeSchema
from app.services.mundane.ingress_service import MundaneIngressService
from app.services.mundane.station_service import MundaneStationService

router = APIRouter()
ephemeris = Ephemeris()


@router.get("/ingresses", response_model=IngressResponse, summary="Get sign ingresses for a planet")
def get_ingresses(
    planet: Planet,
    start_time: datetime = Query(...),
    end_time: datetime | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> IngressResponse:
    """
    Search for sign boundary crossings (0° sign entry) for a planet.
    """
    t_start = Time(start_time)
    t_end = Time(end_time) if end_time else Time(start_time + timedelta(days=365))

    ingress_service = MundaneIngressService(context, ephemeris=ephemeris)
    events = ingress_service.scan_ingresses(planet, t_start, t_end)

    # Map domain MundaneIngress → IngressSchema
    ingresses = [
        IngressSchema(
            planet=e.planet.name,
            time=e.time,
            from_sign=e.from_sign,
            to_sign=e.to_sign,
        )
        for e in events
    ]

    return IngressResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="mundane.ingresses"
        ),
        data=ingresses
    )


@router.get("/retrogrades", response_model=RetrogradeResponse, summary="Get planetary stations")
def get_retrogrades(
    planet: Planet,
    start_time: datetime = Query(...),
    end_time: datetime | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> RetrogradeResponse:
    """
    Search for planetary stations (turning Direct or Retrograde).
    """
    t_start = Time(start_time)
    t_end = Time(end_time) if end_time else Time(start_time + timedelta(days=365))

    if planet in [Planet.SUN, Planet.MOON]:
        return RetrogradeResponse(meta=get_meta(is_sidereal=context.zodiac.is_sidereal, sidereal_mode=context.zodiac.sidereal_mode), data=[])

    station_service = MundaneStationService(context, ephemeris=ephemeris)
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

    return RetrogradeResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="mundane.stations"
        ),
        data=stations
    )
