"""
/api/v2/financial — Advanced Astro Time Windows specifically geared toward classical
financial and market correlations.

**WARNING:** AstroSDK makes no predictions about financial markets. This module
simply computes strictly defined astronomical windows classically associated with
market shifts (e.g. shadow periods, multi-planet retrogrades, major outer
planet ingresses).
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.financial import (
    FinancialEventData,
    FinancialEventResponse,
    FinancialTimeWindowData,
    FinancialTimeWindowResponse,
    TimeWindowSchema,
)
from app.services.mundane.ingress_service import MundaneIngressService
from app.services.mundane.station_service import MundaneStationService
from app.services.research.financial_service import ResearchFinancialService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/time-windows",
    response_model=FinancialTimeWindowResponse,
    summary="Get bounded time windows like retrograde phases.",
)
def get_financial_time_windows(
    start_time: datetime = Query(...),
    max_days: float = Query(365.25, gt=0, le=3650.0),
    planets: list[Planet] | None = Query(None, description="Select explicit planets to tracking."),
    preset: str | None = Query(None, description="Preset configurations. Use 'big_shifts' for major outer planets."),
    context: CalculationContext = Depends(get_calculation_context),
) -> FinancialTimeWindowResponse:
    """
    Calculate retrograde and critical anomaly bounded time windows over a range.
    By default this checks all planets if not specified. Using preset='big_shifts' will lock it to Jupiter, Saturn, Uranus, Neptune, and Pluto.
    """
    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + max_days)

    financial_service = ResearchFinancialService(context, ephemeris)

    if preset == "big_shifts":
        planets = [Planet.JUPITER, Planet.SATURN, Planet.URANUS, Planet.NEPTUNE, Planet.PLUTO]

    windows = financial_service.get_time_windows(t_start, t_end, planets)

    schema_windows = [
        TimeWindowSchema(
            planet=w.planet.name,
            start_time=w.start_time,
            end_time=w.end_time,
            event_type=w.event_type,
            metadata={k: str(v) for k, v in w.metadata.items()},
        )
        for w in windows
    ]

    data = FinancialTimeWindowData(windows=schema_windows)

    return FinancialTimeWindowResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            astro_data_only=True,
            no_financial_advice=True,
            capability="research.financial"
        ),
        data=data,
    )





@router.get("/retrogrades", response_model=FinancialEventResponse)
def get_financial_retrogrades(
    planet: Planet,
    start_time: datetime = Query(...),
    end_time: datetime | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> FinancialEventResponse:
    t_start = Time(start_time)
    if planet in [Planet.SUN, Planet.MOON]:
        return FinancialEventResponse(meta=get_meta(is_sidereal=context.zodiac.is_sidereal, sidereal_mode=context.zodiac.sidereal_mode, astro_data_only=True, no_financial_advice=True), data=FinancialEventData(events=[]))

    station_service = MundaneStationService(context, ephemeris)
    # Search for a long enough window to find next stations
    scan_end = Time.from_julian_day(t_start.julian_day + 400)
    events = station_service.scan_stations(planet, t_start, scan_end)

    mapped = [
        {"planet": planet.name, "time": e.time, "type": e.station_type}
        for e in events if end_time is None or e.time <= end_time
    ]
    return FinancialEventResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            astro_data_only=True,
            no_financial_advice=True,
            capability="mundane.stations"
        ),
        data=FinancialEventData(events=mapped)
    )


@router.get("/ingresses", response_model=FinancialEventResponse)
def get_financial_ingresses(
    planet: Planet,
    start_time: datetime = Query(...),
    end_time: datetime | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> FinancialEventResponse:
    t_start = Time(start_time)
    ingress_service = MundaneIngressService(context, ephemeris)

    # scan roughly a year if no end_time
    # Use 365 days for scan if end_time not provided
    t_end = Time(end_time) if end_time else Time.from_julian_day(t_start.julian_day + 365)
    events = ingress_service.scan_ingresses(planet, t_start, t_end)

    mapped = [
        {"planet": planet.name, "time": e.time, "from_sign": e.from_sign, "to_sign": e.to_sign}
        for e in events
    ]
    return FinancialEventResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            astro_data_only=True,
            no_financial_advice=True,
            capability="mundane.ingresses"
        ),
        data=FinancialEventData(events=mapped)
    )


@router.get("/eclipses", response_model=FinancialEventResponse)
def get_financial_eclipses(
    start_time: datetime = Query(...),
    end_time: datetime | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> FinancialEventResponse:
    t_start = Time(start_time)


    # Native 2.0 find eclipses logic
    results = []
    current_jd = t_start.julian_day
    for _ in range(5):
        res = ephemeris.find_next_eclipse(current_jd, solar=False) # Lunar eclipses primarily for financial classics
        if not res:
            break
        t = Time.from_julian_day(res["peak_jd"])
        if end_time and t.dt > end_time:
            break
        results.append({"time": t.dt, "type": res["type"]})
        current_jd = res["peak_jd"] + 30.0

    return FinancialEventResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            astro_data_only=True,
            no_financial_advice=True,
            capability="astronomy.lunar.eclipses"
        ),
        data=FinancialEventData(events=results)
    )


@router.get("/events", response_model=FinancialEventResponse)
def get_financial_events(
    start_time: datetime = Query(...),
) -> FinancialEventResponse:
    return FinancialEventResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None, astro_data_only=True, no_financial_advice=True), data=FinancialEventData(events=[]))
