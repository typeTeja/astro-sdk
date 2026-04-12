"""
/api/v2/synodic — Exact synodic events (conjunctions, oppositions, any angle).
Re-exports the synodic event finding from SynodicService with a dedicated route.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.synodic import SynodicConjunctionResponse, SynodicConjunctionSchema
from app.services.astronomy.synodic_service import AstronomySynodicService
from app.contexts.factories import create_default_context
from app.api.v2.meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/next",
    response_model=SynodicConjunctionResponse,
    summary="Find the next exact synodic event between two planets",
)
async def get_next_synodic(
    p1: Planet,
    p2: Planet,
    target_angle: float = Query(
        0.0,
        ge=0.0,
        le=360.0,
        description="Target angle in degrees (0=Conjunction, 180=Opposition, 90=Square, etc.)",
    ),
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    max_days: float = Query(1000.0, gt=0.0, le=36525.0),
) -> SynodicConjunctionResponse:
    """
    Find the next time p1 and p2 reach a specific angular separation.
    Uses bisection refinement for sub-minute precision.

    Common angles:
    - 0° = Conjunction (new synodic cycle)
    - 180° = Opposition (full)
    - 90° = Square
    - 120° = Trine
    - 60° = Sextile
    """
    t_start = Time(start_time)
    context = create_default_context()
    synodic_service = AstronomySynodicService(context, ephemeris=ephemeris)
    result = synodic_service.find_next_event(p1, p2, t_start, target_angle, max_days)

    if not result:
        return SynodicConjunctionResponse(
            meta=get_meta(is_sidereal=False, sidereal_mode=None),
            data=None,  # type: ignore[arg-type]
        )

    data = SynodicConjunctionSchema(
        p1=result["p1"],
        p2=result["p2"],
        target_angle=result["target_angle"],
        time=result["time"],
        julian_day=Time(result["time"]).julian_day,
    )
    return SynodicConjunctionResponse(
        meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data
    )



