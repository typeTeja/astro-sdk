from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.charts import PanchangaDataSchema, PanchangaResponse
from app.services.vedic.panchanga_service import VedicPanchangaService

router = APIRouter()
ephemeris = Ephemeris()


@router.get("/panchang", response_model=PanchangaResponse, summary="[V2] Get Vedic Panchang")
def get_panchanga(
    context: Annotated[CalculationContext, Depends(get_calculation_context)],
    time: datetime = Query(...),
) -> PanchangaResponse:
    """
    Calculate the five elements of the Vedic calendar using the 2.0 platform.
    Defaults to Sidereal (Lahiri) if not overridden in headers.
    Requires topocentric coordinates via Header or Query params mapping.
    """
    t = Time(time)

    # Delegate to the native 2.0 service
    service = VedicPanchangaService(context, ephemeris=ephemeris)
    data = service.calculate_panchanga(t)

    return PanchangaResponse(
        meta=get_meta(
            is_sidereal=True,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="vedic.panchanga",
            feature_maturity="PRODUCTION"
        ),
        data=data
    )
