"""
/api/v2/cycles — Advanced planetary combinations and midpoints.
"""
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.base import BaseAstroResponse
from app.services.western.chart_service import WesternChartService

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
def post_cycles_composite(
    request: CompositeRequest,
    context: CalculationContext = Depends(get_calculation_context),
) -> CompositeResponse:
    """
    Accepts a list of planets and returns their midpoint/centroid coordinate
    at a specific point in time.
    """
    t = Time(request.time)
    chart_service = WesternChartService(context, ephemeris=ephemeris)
    chart = chart_service.create_chart(t, context.observer.latitude if context.observer else 0.0, context.observer.longitude if context.observer else 0.0)

    selected_longs = [p.longitude for p in chart.planets if p.planet in request.planets]

    centroid = 0.0 if not selected_longs else sum(selected_longs) / len(selected_longs)

    data = CompositeData(
        time=t.dt,
        composite_longitude=centroid,
        planets_involved=[p.name for p in request.planets]
    )

    return CompositeResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="western.composite"
        ),
        data=data
    )
