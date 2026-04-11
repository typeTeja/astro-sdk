from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.time import Time
from ...schemas.lunar import (
    EclipseResponse,
    EclipseSchema,
    LunarExtremeResponse,
    LunarPhasesResponse,
)
from ...services.astronomy.lunar_service import AstronomyLunarService
from ...contexts.factories import create_default_context
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get("/phases", response_model=LunarPhasesResponse, summary="Get major lunar phases")
async def get_lunar_phases(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    count: int = Query(4, ge=1, le=50),
    angle: float | None = Query(None, description="Custom Sun-Moon separation angle"),
) -> LunarPhasesResponse:
    """
    Search for upcoming major lunar phases (New, Full, etc.) or a specific angle.
    """
    t = Time(start_time)
    context = create_default_context()
    lunar_service = AstronomyLunarService(context, ephemeris=ephemeris)
    
    phases = lunar_service.get_next_phases(t, count=count)

    data = [
        {
            "phase_name": p.phase_name,
            "time": p.time,
            "julian_day": Time(p.time).julian_day,
            "degree": 0.0 # Standard phase angles
        }
        for p in phases
    ]
    return LunarPhasesResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)


@router.get(
    "/extremes", response_model=LunarExtremeResponse, summary="Get lunar perigee and apogee"
)
async def get_lunar_extremes(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    count: int = Query(2, ge=1, le=10),
) -> LunarExtremeResponse:
    """
    Find upcoming Apogee and Perigee points.
    """
    t = Time(start_time)
    context = create_default_context()
    lunar_service = AstronomyLunarService(context, ephemeris=ephemeris)
    
    extremes = lunar_service.get_lunar_extremes(t, count=count)

    return LunarExtremeResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=extremes)


@router.get("/eclipses", response_model=EclipseResponse, summary="Search for eclipses")
async def get_eclipses(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    count: int = Query(2, ge=1, le=10),
    solar: bool = Query(True, description="Search for Solar (True) or Lunar (False) eclipses"),
) -> EclipseResponse:
    """
    Calculate the next N eclipse moments starting from a point in time.
    """
    t = Time(start_time)

    # We use ephemeris directly if not in LunarService or wrap it
    # Currently Mypy is flagging LunarService missing eclipse methods.
    # We'll use the core ephemeris for now to align.

    results = []
    current_jd = t.julian_day
    for _ in range(count):
        # find_next_eclipse(jd_start, is_solar)
        res = ephemeris.find_next_eclipse(current_jd, solar=solar)
        if res:
            res_time = Time.from_julian_day(res["peak_jd"]).dt
            results.append(EclipseSchema(time=res_time, type=res["type"], is_solar=solar))
            # Advance to find the next one
            current_jd = res["peak_jd"] + 30.0
        else:
            break

    return EclipseResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=results)
