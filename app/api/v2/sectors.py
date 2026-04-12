from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.charts import NatalChartRequest
from app.schemas.vedic import SectorHitSchema, SectorResponse
from app.services.astronomy.sector_service import AstronomySectorService

router = APIRouter()
ephemeris = Ephemeris()


@router.post("/gauquelin", response_model=SectorResponse, summary="Calculate planetary sectors")
def get_gauquelin_sectors(
    request: NatalChartRequest,
    num_sectors: int = Query(36, ge=12, le=36),
    context: CalculationContext = Depends(get_calculation_context),
) -> SectorResponse:
    """
    Calculate the planetary sector occupancy for a given chart and time.
    Standard Gauquelin research uses 12, 18, or 36 sectors.
    """
    t = Time(request.time.time)
    sector_service = AstronomySectorService(context, ephemeris=ephemeris)

    raw = sector_service.get_sectors(
        t,
        context.observer.latitude if context.observer else request.location.latitude,
        context.observer.longitude if context.observer else request.location.longitude,
        num_sectors=num_sectors
    )

    data = [
        SectorHitSchema(planet=r["planet"], sector=r["sector"], intensity=r["intensity"])
        for r in raw
    ]

    return SectorResponse(
        meta=get_meta(
            capability="astronomy.sectors.gauquelin",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )
