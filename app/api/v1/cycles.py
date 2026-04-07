"""
/api/v1/cycles — Advanced planetary combinations and midpoints.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.base import BaseAstroResponse
from ...services.natal_service import NatalService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
natal_service = NatalService(ephemeris)


class CompositeRequest(BaseModel):
    planets: list[Planet]
    time: datetime


class CompositeData(BaseModel):
    time: datetime
    composite_longitude: float
    planets_involved: list[str]


class CompositeResponse(BaseAstroResponse[CompositeData]):
    pass


@router.post(
    "/composite",
    response_model=CompositeResponse,
    summary="[EXPERIMENTAL] Composite Centroid",
    description="**EXPERIMENTAL API:** This calculates a simple spherical arithmetic mean of the requested planets' longitudes. It does not perform true spatial or declination-weighted centroids.",
)
async def post_cycles_composite(
    request: CompositeRequest,
    is_sidereal: bool = Query(True),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> CompositeResponse:
    """
    Accepts a list of planets and returns their midpoint/centroid coordinate
    at a specific point in time.
    """
    t = Time(request.time)
    
    positions = natal_service.calculate_positions(t, sidereal_mode if is_sidereal else None)
    
    selected_longs = []
    for pos in positions:
        if pos.planet in request.planets:
            selected_longs.append(pos.longitude)
            
    if not selected_longs:
        centroid = 0.0
    else:
        # Simple arithmetic mean of longitudes for the basic composite structure
        # Advanced spherical midpoint mathematics can be subbed in later.
        centroid = sum(selected_longs) / len(selected_longs)

    data = CompositeData(
        time=t.dt,
        composite_longitude=centroid,
        planets_involved=[p.name for p in request.planets]
    )

    return CompositeResponse(
        meta=get_meta(is_sidereal=is_sidereal, sidereal_mode=sidereal_mode), 
        data=data
    )
