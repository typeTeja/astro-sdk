from typing import Any

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.astro import PlanetPositionData
from app.schemas.charts import NatalChartRequest
from app.schemas.vedic import (
    AshtakavargaData,
    AshtakavargaResponse,
    DashaPeriodSchema,
    DashaResponse,
    DChartData,
    DChartResponse,
    PlanetaryStrengthSchema,
    ShadbalaResponse,
)
from app.services.vedic.ashtakavarga_service import VedicAshtakavargaService
from app.services.vedic.dasha_service import VedicDashaService
from app.services.vedic.shadbala_service import VedicShadbalaService
from app.services.vedic.varga_service import VedicVargaService

router = APIRouter()
ephemeris = Ephemeris()


@router.post(
    "/divisional", response_model=DChartResponse, summary="Calculate a varga (divisional chart)"
)
def get_varga(
    request: NatalChartRequest,
    division: int = Query(9, ge=1, le=150),
    context: CalculationContext = Depends(get_calculation_context)
) -> DChartResponse:
    """
    Calculate planetary positions for a Vedic divisional chart.

    Professional-grade elements:
    - D9 (Navamsa) uses traditional element-based cycle logic (Ar-Cp-Li-Can).
    - All charts strictly follow sidereal standards.
    """
    t = Time(request.time.time)

    # 2.0 Standard: Vedic defaults to Sidereal if not explicitly overridden by headers/query
    if not context.zodiac.is_sidereal and "X-Astro-Is-Sidereal" not in context.fingerprint:
         from app.contexts.zodiac import ZodiacType
         context.zodiac.zodiac = ZodiacType.SIDEREAL
         context.zodiac.sidereal_mode = SiderealMode.LAHIRI

    varga_service = VedicVargaService(context)
    positions = varga_service.calculate_varga_positions(t, division)

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
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="vedic.varga"
        ),
        data=DChartData(division=division, planets=planets_data)
    )


@router.post("/dashas", response_model=DashaResponse, summary="Calculate predictive dasha periods")
def get_dashas(
    request: NatalChartRequest,
    cycles: int = Query(1, ge=1, le=2),
    levels: int = Query(2, ge=1, le=2, description="Level 1 = Mahadasha, Level 2 = Antardasha"),
    context: CalculationContext = Depends(get_calculation_context)
) -> DashaResponse:
    """
    Calculate Vimshottari dasha periods for a birth chart.
    """
    t = Time(request.time.time)

    # 2.0 Standard: Vedic defaults to Sidereal if not explicitly overridden by headers/query
    if not context.zodiac.is_sidereal and "X-Astro-Is-Sidereal" not in context.fingerprint:
         from app.contexts.zodiac import ZodiacType
         context.zodiac.zodiac = ZodiacType.SIDEREAL
         context.zodiac.sidereal_mode = SiderealMode.LAHIRI

    dasha_service = VedicDashaService(context)
    domain_dashas = dasha_service.calculate_mahadashas(t) # Simplified for v1

    def _map_dasha(d: Any) -> DashaPeriodSchema:
        return DashaPeriodSchema(
            lord=d.lord.name if hasattr(d.lord, "name") else str(d.lord),
            start_time=d.start,
            end_time=d.end,
            level=d.level,
            sub_periods=[_map_dasha(sub) for sub in d.sub_periods] if hasattr(d, "sub_periods") and d.sub_periods else None,
        )

    dashas = [_map_dasha(d) for d in domain_dashas]
    return DashaResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="vedic.dashas"
        ),
        data=dashas
    )


@router.post(
    "/shadbala", response_model=ShadbalaResponse, summary="[EXPERIMENTAL] Shadbala Planetary Strength"
)
def get_shadbala(
    request: NatalChartRequest,
    context: CalculationContext = Depends(get_calculation_context)
) -> ShadbalaResponse:
    """
    Evaluates the 6-fold planetary strength routing matrix.
    """
    t = Time(request.time.time)

    # 2.0 Standard: Vedic defaults to Sidereal if not explicitly overridden by headers/query
    if not context.zodiac.is_sidereal and "X-Astro-Is-Sidereal" not in context.fingerprint:
         from app.contexts.zodiac import ZodiacType
         context.zodiac.zodiac = ZodiacType.SIDEREAL
         context.zodiac.sidereal_mode = SiderealMode.LAHIRI

    # We need a chart for shadbala
    from app.services.western import WesternChartService
    chart_service = WesternChartService(context, ephemeris=ephemeris)
    chart = chart_service.create_chart(t, request.location.latitude, request.location.longitude)

    shadbala_service = VedicShadbalaService(context)
    domain_scores = shadbala_service.calculate_shadbala(chart.planets, chart.houses.axes.ascendant if chart.houses and chart.houses.axes else 0.0)

    mapped = [
        PlanetaryStrengthSchema(
            planet=s.planet,
            positional_strength=s.total_rupas / 6.0, # Approximate mapping to legacy fields
            directional_strength=s.total_rupas / 6.0,
            temporal_strength=0.0,
            motional_strength=0.0,
            natural_strength=0.0,
            aspectual_strength=0.0,
            total_rupas=s.total_rupas,
        ) for s in domain_scores
    ]
    return ShadbalaResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            experimental=True,
            capability="vedic.shadbala"
        ),
        data=mapped
    )


@router.post(
    "/ashtakavarga", response_model=AshtakavargaResponse, summary="[EXPERIMENTAL] Ashtakavarga Array"
)
def get_ashtakavarga(
    request: NatalChartRequest,
    context: CalculationContext = Depends(get_calculation_context)
) -> AshtakavargaResponse:
    """
    Evaluates the basic bindu transit scoring matrix.
    """
    t = Time(request.time.time)

    if not context.zodiac.is_sidereal and "X-Astro-Is-Sidereal" not in context.fingerprint:
         from app.contexts.zodiac import ZodiacType
         context.zodiac.zodiac = ZodiacType.SIDEREAL
         context.zodiac.sidereal_mode = SiderealMode.LAHIRI

    from app.services.western import WesternChartService
    chart_service = WesternChartService(context, ephemeris=ephemeris)
    chart = chart_service.create_chart(t, request.location.latitude, request.location.longitude)

    av_service = VedicAshtakavargaService(context)
    domain_matrix = av_service.calculate_sav(chart.planets, chart.houses.axes.ascendant if chart.houses and chart.houses.axes else 0.0)

    # Simplified mapping to legacy matrix if needed
    data = AshtakavargaData(matrix={"SAV": domain_matrix.matrix})
    return AshtakavargaResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            experimental=True,
            capability="vedic.ashtakavarga"
        ),
        data=data
    )
