from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.astro import PlanetPositionData
from ...schemas.charts import NatalChartRequest
from ...schemas.vedic import DashaResponse, DChartData, DChartResponse
from ...services.vedic_service import VedicService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
vedic_service = VedicService(ephemeris)


@router.post(
    "/divisional", response_model=DChartResponse, summary="Calculate a varga (divisional chart)"
)
async def get_varga(
    request: NatalChartRequest, division: int = Query(9, ge=1, le=150)
) -> DChartResponse:
    """
    Calculate planetary positions for a Vedic divisional chart.

    Professional-grade elements:
    - D9 (Navamsa) use traditional element-based cycle logic (Ar-Cp-Li-Can).
    - All charts strictly follow sidereal standards.
    """
    t = Time(request.time.time)

    # Resolve settings with defaults
    mode = SiderealMode.LAHIRI
    if request.settings and "sidereal_mode" in request.settings:
        mode = SiderealMode(request.settings["sidereal_mode"])

    # Returns list[PlanetPosition]
    positions = vedic_service.calculate_varga_positions(t, division, sidereal_mode=mode)

    # Map domain positions to schema data
    planets_data = [
        PlanetPositionData(
            planet=str(p.planet),
            longitude=p.longitude,
            latitude=p.latitude,
            distance=p.distance,
            speed_long=p.speed_long,
            is_retrograde=p.is_retrograde,
            sign=p.sign,
            sign_name=PlanetPositionData.get_sign_name(p.longitude),
        )
        for p in positions
    ]

    return DChartResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=mode),
        data=DChartData(division=division, planets=planets_data),
    )


@router.post("/dashas", response_model=DashaResponse, summary="Calculate predictive dasha periods")
async def get_dashas(
    request: NatalChartRequest,
    cycles: int = Query(1, ge=1, le=2),
    levels: int = Query(2, ge=1, le=2, description="Level 1 = Mahadasha, Level 2 = Antardasha"),
) -> DashaResponse:
    """
    Calculate Vimshottari dasha periods for a birth chart.

    Features:
    - Level 1: Primary Mahadashas (120-year cycle).
    - Level 2: Secondary Antardashas ( Bhuktis).
    """
    t = Time(request.time.time)

    # Resolve settings with defaults
    mode = SiderealMode.LAHIRI
    if request.settings and "sidereal_mode" in request.settings:
        mode = SiderealMode(request.settings["sidereal_mode"])

    dashas = vedic_service.calculate_dashas(t, cycles, levels, sidereal_mode=mode)

    return DashaResponse(meta=get_meta(is_sidereal=True, sidereal_mode=mode), data=dashas)
