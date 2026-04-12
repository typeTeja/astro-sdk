from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.charts import PanchangaData, PanchangaResponse
from app.services.vedic.panchanga_service import VedicPanchangaService

router = APIRouter()
ephemeris = Ephemeris()


@router.get("/panchang", response_model=PanchangaResponse, summary="[V2] Get Vedic Panchang")
async def get_panchanga(
    context: Annotated[CalculationContext, Depends(get_calculation_context)],
    latitude: float = Query(...),
    longitude: float = Query(...),
    altitude: float = Query(0.0),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> PanchangaResponse:
    """
    Calculate the five elements of the Vedic calendar using the 2.0 platform.
    Defaults to Sidereal (Lahiri) if not overridden in headers.
    """
    t = Time(time)
    
    # Delegate to the native 2.0 service
    service = VedicPanchangaService(context, ephemeris=ephemeris)
    results = service.calculate_panchanga(t, latitude, longitude, altitude)
    
    # results is a PanchangaData domain model, we need to return it in the expected response format
    # The response expects data: PanchangaData (which results is)
    return PanchangaResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=context.zodiac.sidereal_mode),
        data=results
    )
