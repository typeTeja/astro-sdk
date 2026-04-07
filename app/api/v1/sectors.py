from fastapi import APIRouter, Query

from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.charts import NatalChartRequest
from ...schemas.vedic import SectorResponse
from ...services.sector_engine import SectorEngine
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
sector_engine = SectorEngine(ephemeris)


@router.post("/gauquelin", response_model=SectorResponse, summary="Calculate planetary sectors")
async def get_gauquelin_sectors(
    request: NatalChartRequest, num_sectors: int = Query(36, ge=12, le=36)
) -> SectorResponse:
    """
    Calculate the planetary sector occupancy for a given chart and time.
    Standard Gauquelin research uses 12, 18, or 36 sectors.
    """
    t = Time(request.time.time)

    # Sectors are observational/geocentric
    results = sector_engine.calculate_sectors(
        t, request.location.latitude, request.location.longitude, num_sectors=num_sectors
    )

    return SectorResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=results)
