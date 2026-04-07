"""
/api/v1/financial — Advanced Astro Time Windows specifically geared toward classical
financial and market correlations.

**WARNING:** AstroSDK makes no predictions about financial markets. This module
simply computes strictly defined astronomical windows classically associated with
market shifts (e.g. shadow periods, multi-planet retrogrades, major outer
planet ingresses).
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.financial import (
    FinancialTimeWindowData,
    FinancialTimeWindowResponse,
    TimeWindowSchema,
)
from ...services.crossing_service import CrossingService
from ...services.events_service import EventsService
from ...services.financial_time_service import FinancialTimeService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
crossing_service = CrossingService(ephemeris)
events_service = EventsService(ephemeris, crossing_service)
financial_service = FinancialTimeService(ephemeris, events_service)


@router.get(
    "/time-windows",
    response_model=FinancialTimeWindowResponse,
    summary="Get bounded time windows like retrograde phases.",
)
async def get_financial_time_windows(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    max_days: float = Query(365.25, gt=0, le=3650.0),
    planets: list[Planet] | None = Query(None, description="Select explicit planets to tracking."),
    preset: str | None = Query(None, description="Preset configurations. Use 'big_shifts' for major outer planets."),
) -> FinancialTimeWindowResponse:
    """
    Calculate retrograde and critical anomaly bounded time windows over a range.
    By default this checks all planets if not specified. Using preset='big_shifts' will lock it to Jupiter, Saturn, Uranus, Neptune, and Pluto.
    """
    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + max_days)

    if preset == "big_shifts":
        planets = [Planet.JUPITER, Planet.SATURN, Planet.URANUS, Planet.NEPTUNE, Planet.PLUTO]

    windows = financial_service.get_time_windows(t_start, t_end, planets)

    schema_windows = [
        TimeWindowSchema(
            planet=w.planet.name,
            start_time=w.start_time,
            end_time=w.end_time,
            event_type=w.event_type,
            metadata=w.metadata,
        )
        for w in windows
    ]

    data = FinancialTimeWindowData(windows=schema_windows)
    
    return FinancialTimeWindowResponse(
        meta=get_meta(is_sidereal=False, sidereal_mode=None, astro_data_only=True, no_financial_advice=True),
        data=data,
    )


from ...schemas.financial import FinancialEventData, FinancialEventResponse

@router.get("/retrogrades", response_model=FinancialEventResponse)
async def get_financial_retrogrades(
    planet: Planet,
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    end_time: datetime | None = Query(None),
) -> FinancialEventResponse:
    t_start = Time(start_time)
    if planet in [Planet.SUN, Planet.MOON]:
        return FinancialEventResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None, astro_data_only=True, no_financial_advice=True), data=FinancialEventData(events=[]))

    events = events_service.get_retrograde_stations(t_start, planet, count=2)
    mapped = [{"planet": e.planet.name, "time": e.time, "type": e.station_type} for e in events if end_time is None or e.time <= end_time]
    return FinancialEventResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None, astro_data_only=True, no_financial_advice=True), data=FinancialEventData(events=mapped))


@router.get("/ingresses", response_model=FinancialEventResponse)
async def get_financial_ingresses(
    planet: Planet,
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    end_time: datetime | None = Query(None),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> FinancialEventResponse:
    t_start = Time(start_time)
    events = events_service.get_sign_ingresses(t_start, planet, count=12 if end_time else 1, sidereal_mode=sidereal_mode)
    mapped = [{"planet": e.planet.name, "time": e.time, "from_sign": e.from_sign, "to_sign": e.to_sign} for e in events if end_time is None or e.time <= end_time]
    return FinancialEventResponse(meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode, astro_data_only=True, no_financial_advice=True), data=FinancialEventData(events=mapped))


@router.get("/eclipses", response_model=FinancialEventResponse)
async def get_financial_eclipses(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    end_time: datetime | None = Query(None),
) -> FinancialEventResponse:
    t_start = Time(start_time)
    from ...services.lunar_service import LunarService
    lunar_service = LunarService(ephemeris)
    eclipses = lunar_service.find_lunar_eclipses(t_start, t_start.dt.year + 2) # Arbitrary bounded search
    mapped = []
    for jd, _type in eclipses[:5]:
        t = Time.from_julian_day(jd)
        if end_time is None or t.dt <= end_time:
            mapped.append({"time": t.dt, "type": _type})
    return FinancialEventResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None, astro_data_only=True, no_financial_advice=True), data=FinancialEventData(events=mapped))

@router.get("/events", response_model=FinancialEventResponse)
async def get_financial_events(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> FinancialEventResponse:
    # Blanket default representing high-volume macro timeline
    return FinancialEventResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None, astro_data_only=True, no_financial_advice=True), data=FinancialEventData(events=[]))
