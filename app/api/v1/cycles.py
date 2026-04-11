"""
/api/v1/cycles — Advanced planetary combinations and midpoints.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ...core.time import Time
from ...schemas.base import BaseAstroResponse
from ...services.western.chart_service import WesternChartService
from ...contexts.factories import create_default_context
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


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
    context = create_default_context()
    context.zodiac.is_sidereal = is_sidereal
    context.zodiac.sidereal_mode = sidereal_mode
    
    chart_service = WesternChartService(context, ephemeris=ephemeris)
    chart = chart_service.create_chart(t, 0.0, 0.0)
    
    selected_longs = [p.longitude for p in chart.planets if p.planet in request.planets]
            
    if not selected_longs:
        centroid = 0.0
    else:
        # Simple arithmetic mean of longitudes
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
