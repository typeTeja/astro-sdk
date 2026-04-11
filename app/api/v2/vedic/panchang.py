from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from ....contexts.calculation import CalculationContext
from ....core.time import Time
from ....schemas.charts import PanchangaResponse, PanchangaData
from ....services.panchanga_service import PanchangaService
from ..common import get_calculation_context

router = APIRouter()


@router.get("/panchang", response_model=PanchangaResponse, summary="[V2] Get Vedic Panchang")
async def get_panchanga(
    context: Annotated[CalculationContext, Depends(get_calculation_context)],
    latitude: float = Query(...),
    longitude: float = Query(...),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> PanchangaResponse:
    """
    Calculate the five elements of the Vedic calendar using the 2.0 platform.
    Defaults to Sidereal (Lahiri) if not overridden in headers.
    """
    t = Time(time)
    
    # Delegate to the high-level service
    # In v2, PanchangaService would be refactored to take the context
    # but for now we use the adapter
    from ....core.ephemeris import Ephemeris
    eph = Ephemeris()
    service = PanchangaService(eph)
    
    results = service.calculate_panchanga(t, latitude, longitude)
    
    return {
        "data": results,
        "meta": {
            "is_sidereal": True,
            "sidereal_mode": "LAHIRI",
            "calculation_fingerprint": context.fingerprint
        }
    }
