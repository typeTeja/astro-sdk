from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet, validate_enum_by_name
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.api.v2.common import get_calculation_context

router = APIRouter()
ephemeris = Ephemeris()


@router.get("/planet-position", summary="[V2] Get single planet position")
async def get_planet_position(
    planet: str,
    context: Annotated[CalculationContext, Depends(get_calculation_context)],
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> dict:
    """
    Get raw astronomical position for a planet with full 2.0 context awareness.
    """
    t = Time(time)
    
    # Resolve planet name
    p_enum = validate_enum_by_name(Planet, planet)
    
    # Sidereal check from context
    is_sidereal = context.zodiac.zodiac == "sidereal" or context.zodiac.sidereal_mode is not None
    
    # We use the raw ephemeris for the most basic position
    pos = ephemeris.calculate_planet(t.julian_day, p_enum, sidereal=is_sidereal)
    
    return {
        "planet": p_enum.name,
        "time": t.dt.isoformat(),
        "position": pos,
        "fingerprint": context.fingerprint # Capability reporting
    }
