from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.transits import SecondaryProgressionResponse
from ...services.progression_service import ProgressionService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
progression_service = ProgressionService(ephemeris)


@router.get(
    "/secondary",
    response_model=SecondaryProgressionResponse,
    summary="Get secondary progression positions",
)
async def get_secondary_progression(
    birth_time: datetime = Query(...),
    target_date: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> SecondaryProgressionResponse:
    """
    Calculate Secondary Progressions (Day-for-a-Year) for a given life moment.
    """
    t_birth = Time(birth_time)
    t_target = Time(target_date)

    # 1. Calculate progressions (Now returns SecondaryProgressionData schema object)
    data = progression_service.calculate_secondary_progression(
        t_birth, t_target, sidereal_mode=sidereal_mode
    )

    return SecondaryProgressionResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode), data=data
    )
