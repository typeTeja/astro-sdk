from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.astro import PlanetPositionData
from ...schemas.charts import NatalChartRequest
from ...schemas.vedic import DashaPeriodSchema, DashaResponse, DChartData, DChartResponse
from ...services.vedic_service import DashaPeriod, VedicService
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
    - D9 (Navamsa) uses traditional element-based cycle logic (Ar-Cp-Li-Can).
    - All charts strictly follow sidereal standards.
    """
    t = Time(request.time.time)

    mode = SiderealMode.LAHIRI
    if request.settings and "sidereal_mode" in request.settings:
        mode = SiderealMode(request.settings["sidereal_mode"])

    # Returns list[PlanetPosition] domain objects
    positions = vedic_service.calculate_varga_positions(t, division, sidereal_mode=mode)

    # Map domain PlanetPosition → PlanetPositionData schema
    planets_data = [
        PlanetPositionData(
            planet=p.planet.name,
            longitude=p.longitude,
            latitude=p.latitude,
            distance=p.distance,
            speed_long=p.speed_long,
            is_retrograde=p.is_retrograde,
            sign=p.sign + 1,
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
    - Level 2: Secondary Antardashas (Bhuktis).
    """
    t = Time(request.time.time)

    mode = SiderealMode.LAHIRI
    if request.settings and "sidereal_mode" in request.settings:
        mode = SiderealMode(request.settings["sidereal_mode"])

    # Returns list[DashaPeriod] domain objects
    domain_dashas = vedic_service.calculate_dashas(t, cycles, levels, sidereal_mode=mode)

    def _map_dasha(d: DashaPeriod) -> DashaPeriodSchema:
        """Map domain DashaPeriod → DashaPeriodSchema (schema layer responsibility)."""
        return DashaPeriodSchema(
            lord=d.lord,
            start_time=d.start_time,
            end_time=d.end_time,
            level=d.level,
            sub_periods=[_map_dasha(sub) for sub in d.sub_periods] if d.sub_periods else None,
        )

    dashas = [_map_dasha(d) for d in domain_dashas]
    return DashaResponse(meta=get_meta(is_sidereal=True, sidereal_mode=mode), data=dashas)

from ...schemas.vedic import ShadbalaResponse, AshtakavargaResponse, AshtakavargaData, PlanetaryStrengthSchema
from ...services.vedic_service import AdvancedVedicService

@router.post(
    "/shadbala", response_model=ShadbalaResponse, summary="[EXPERIMENTAL] Shadbala Planetary Strength"
)
async def get_shadbala(
    request: NatalChartRequest,
) -> ShadbalaResponse:
    """
    Evaluates the 6-fold planetary strength routing matrix.
    """
    t = Time(request.time.time)
    mode = SiderealMode(request.settings.get("sidereal_mode", SiderealMode.LAHIRI.value)) if request.settings else SiderealMode.LAHIRI
    
    advanced_service = AdvancedVedicService(ephemeris)
    domain_strengths = advanced_service.calculate_shadbala(t, mode)

    mapped = [
        PlanetaryStrengthSchema(
            planet=s.planet,
            positional_strength=s.positional_strength,
            directional_strength=s.directional_strength,
            temporal_strength=s.temporal_strength,
            motional_strength=s.motional_strength,
            natural_strength=s.natural_strength,
            aspectual_strength=s.aspectual_strength,
            total_rupas=s.total_rupas,
        ) for s in domain_strengths
    ]
    return ShadbalaResponse(
        meta=get_meta(
            is_sidereal=True,
            sidereal_mode=mode,
            experimental=True,
            algorithm_status="partial",
            requires_domain_validation=True
        ),
        data=mapped
    )


@router.post(
    "/ashtakavarga", response_model=AshtakavargaResponse, summary="[EXPERIMENTAL] Ashtakavarga Array"
)
async def get_ashtakavarga(
    request: NatalChartRequest,
) -> AshtakavargaResponse:
    """
    Evaluates the basic bindu transit scoring matrix.
    """
    t = Time(request.time.time)
    mode = SiderealMode(request.settings.get("sidereal_mode", SiderealMode.LAHIRI.value)) if request.settings else SiderealMode.LAHIRI
    
    advanced_service = AdvancedVedicService(ephemeris)
    domain_matrix = advanced_service.calculate_ashtakavarga(t, mode)

    data = AshtakavargaData(matrix=domain_matrix)
    return AshtakavargaResponse(
        meta=get_meta(
            is_sidereal=True,
            sidereal_mode=mode,
            experimental=True,
            algorithm_status="stub",
            requires_domain_validation=True
        ),
        data=data
    )
