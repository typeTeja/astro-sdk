"""
/api/v2/projections — Mathematical time-based forward projections.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.base import BaseAstroResponse

router = APIRouter()
ephemeris = Ephemeris()


class ProjectionPoint(BaseModel):
    time: datetime
    degree_offset: float | None = None
    time_offset_days: float | None = None


class ProjectionResponseData(BaseModel):
    subject: str
    points: list[ProjectionPoint]


class ProjectionResponse(BaseAstroResponse[ProjectionResponseData]):
    pass


@router.get(
    "/time-swing",
    response_model=ProjectionResponse,
    summary="[EXPERIMENTAL] Time-Swing Projection",
    description="**EXPERIMENTAL API:** This calculates pure, constant time-step intervals (e.g., exactly +90.0 days per step) from a given start date. It does not factor in planetary speed fluctuations or retrograde warping.",
)
def get_time_swing(
    start_time: datetime = Query(...),
    interval_days: float = Query(90.0, gt=0, description="Step duration in days"),
    iterations: int = Query(4, ge=1, le=100),
    context: CalculationContext = Depends(get_calculation_context),
) -> ProjectionResponse:
    """
    Steps forward in uniform time intervals from a seed point.
    """
    t_start = Time(start_time)
    points = []

    for i in range(1, iterations + 1):
        target_jd = t_start.julian_day + (interval_days * i)
        target_time = Time.from_julian_day(target_jd)
        points.append(
            ProjectionPoint(
                time=target_time.dt,
                time_offset_days=interval_days * i
            )
        )

    data = ProjectionResponseData(subject="time_swing", points=points)
    return ProjectionResponse(
        meta=get_meta(
            capability="research.projections.time_swing",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )


@router.get(
    "/synodical-lines",
    response_model=ProjectionResponse,
    summary="[EXPERIMENTAL] Synodical Lines Projection",
    description="**EXPERIMENTAL API:** This projection currently utilizes basic **Mean Daily Motion** approximations to estimate when a planet will hit a specific angle offset. It does *not* utilize rigorous multi-pass inverse bisection, and therefore errors will compound significantly during retrograde stations. Use only for macro structural framing.",
)
def get_synodical_lines(
    planet: Planet,
    start_time: datetime = Query(...),
    interval_degrees: float = Query(90.0, gt=0, description="Angle interval for projection"),
    iterations: int = Query(4, ge=1, le=12),
    context: CalculationContext = Depends(get_calculation_context),
) -> ProjectionResponse:
    """
    Projects when a planet will hit successive degree intervals from its current position.
    """
    t_start = Time(start_time)
    # Stub: returns arbitrary time-offset based on average mean daily motion
    # Since solving the inverse positional transit involves heavy bisection scaling,
    # this fulfills the structural API contract.
    mean_speed_map = {
        Planet.SUN: 0.98,
        Planet.MOON: 13.17,
        Planet.MERCURY: 1.38,
        Planet.VENUS: 1.20,
        Planet.MARS: 0.52,
        Planet.JUPITER: 0.08,
        Planet.SATURN: 0.03,
        Planet.URANUS: 0.01,
        Planet.NEPTUNE: 0.005,
        Planet.PLUTO: 0.003,
    }
    speed = mean_speed_map.get(planet, 1.0)

    points = []
    for i in range(1, iterations + 1):
        target_angle = interval_degrees * i
        estimated_days = target_angle / speed
        target_time = Time.from_julian_day(t_start.julian_day + estimated_days)
        points.append(
            ProjectionPoint(
                time=target_time.dt,
                degree_offset=target_angle
            )
        )

    data = ProjectionResponseData(subject=f"synodical_line_{planet.name}", points=points)
    return ProjectionResponse(
        meta=get_meta(
            capability="research.projections.synodical",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )
