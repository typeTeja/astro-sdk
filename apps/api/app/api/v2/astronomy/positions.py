from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet, validate_enum_by_name
from app.core.time import Time
from app.services.astronomy.planetary_service import AstronomyPlanetaryService

router = APIRouter()


@router.get("/planet-position", summary="[V2] Get single planet position")
def get_planet_position(
    planet: str,
    context: Annotated[CalculationContext, Depends(get_calculation_context)],
    time: datetime = Query(...),
) -> dict[str, Any]:
    """
    Get raw astronomical position for a planet with full 2.0 context awareness.
    """
    t = Time(time)
    p_enum = validate_enum_by_name(Planet, planet)

    # Use the service layer for consistent logic and state management
    service = AstronomyPlanetaryService(context)
    results = service.calculate_positions(t, [p_enum])
    snapshot = results[0]

    return {
        "planet": snapshot.planet.name,
        "time": t.dt.isoformat(),
        "position": {
            "longitude": snapshot.longitude,
            "latitude": snapshot.latitude,
            "distance": snapshot.distance,
            "speed_long": snapshot.speed_long,
        },
        "fingerprint": context.fingerprint
    }
