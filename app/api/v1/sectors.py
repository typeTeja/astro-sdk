from fastapi import APIRouter, Query

from ...core.time import Time
from ...schemas.charts import NatalChartRequest
from ...schemas.vedic import SectorResponse, SectorHitSchema
from ...services.astronomy.sector_service import AstronomySectorService
from ...contexts.factories import create_default_context
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.post("/gauquelin", response_model=SectorResponse, summary="Calculate planetary sectors")
async def get_gauquelin_sectors(
    request: NatalChartRequest, num_sectors: int = Query(36, ge=12, le=36)
) -> SectorResponse:
    """
    Calculate the planetary sector occupancy for a given chart and time.
    Standard Gauquelin research uses 12, 18, or 36 sectors.
    """
    t = Time(request.time.time)
    context = create_default_context()
    sector_service = AstronomySectorService(context, ephemeris=ephemeris)

    raw = sector_service.get_sectors(
        t, request.location.latitude, request.location.longitude, num_sectors=num_sectors
    )

    data = [
        SectorHitSchema(planet=r["planet"], sector=r["sector"], intensity=r["intensity"])
        for r in raw
    ]

    return SectorResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)
