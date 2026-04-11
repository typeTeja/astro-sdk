from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...contexts import FeatureMaturity
from ...schemas.astro import PlanetPositionData
from ...schemas.charts import NatalChartRequest
from ...schemas.transits import SecondaryProgressionData, SecondaryProgressionResponse
from ...services.western import WesternProgressionService
from ...services.western.chart_service import WesternChartService
from ...services.western.aspect_service import WesternAspectService
from ...contexts.factories import create_default_context
from ..common import build_western_chart_context, calculation_metadata
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/secondary",
    response_model=SecondaryProgressionResponse,
    summary="Get secondary progression positions",
)
async def get_secondary_progression(
    birth_time: datetime = Query(...),
    target_date: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
    is_sidereal: bool = Query(True),
) -> SecondaryProgressionResponse:
    """
    Calculate Secondary Progressions (Day-for-a-Year) for a given life moment.
    """
    t_birth = Time(birth_time)
    t_target = Time(target_date)
    context = build_western_chart_context(
        sidereal_mode=sidereal_mode,
        is_sidereal=is_sidereal,
        capability="western.progression",
        maturity=FeatureMaturity.BETA,
    )
    progression_service = WesternProgressionService(context, ephemeris=ephemeris)

    # 1. Calculate progressions → returns ProgressedChart domain object
    prog = progression_service.calculate_secondary_progression(t_birth, t_target)
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "birth_time": t_birth.dt.isoformat(),
            "target_date": t_target.dt.isoformat(),
        },
    )

    # 2. Map domain dict records → PlanetPositionData schemas (schema layer)
    planets_data = [
        PlanetPositionData(
            planet=str(p["planet"]),
            longitude=float(p["longitude"]),  # type: ignore[arg-type]
            latitude=float(p["latitude"]),  # type: ignore[arg-type]
            distance=float(p["distance"]),  # type: ignore[arg-type]
            speed_long=float(p["speed_long"]),  # type: ignore[arg-type]
            is_retrograde=bool(p["is_retrograde"]),
            sign=int(p["sign"]),  # type: ignore[arg-type]
            sign_name=str(p["sign_name"]),
        )
        for p in prog.planets
    ]

    data = SecondaryProgressionData(
        progression_date=prog.progression_date,
        planets=planets_data,
    )

    return SecondaryProgressionResponse(
        meta=get_meta(
            is_sidereal=is_sidereal,
            sidereal_mode=sidereal_mode if is_sidereal else None,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=data,
    )

from ...schemas.transits import TransitScanResponse, TransitScanData, TransitAspectSchema
from ...services.transit_service import TransitService

@router.post(
    "/aspects",
    response_model=TransitScanResponse,
    summary="Scan valid aspects between progressed planets and natal chart",
)
async def get_progression_aspects(
    request: NatalChartRequest,
    target_date: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> TransitScanResponse:
    """
    Scans the progressed state against the natal chart structure.
    Returns domain transit aspects mapping progressed planets.
    """
    t_birth = Time(request.time.time)
    t_target = Time(target_date)
    
    context = create_default_context()
    context.zodiac.is_sidereal = True
    context.zodiac.sidereal_mode = sidereal_mode
    
    chart_service = WesternChartService(context, ephemeris=ephemeris)
    progression_service = WesternProgressionService(context, ephemeris=ephemeris)
    aspect_service = WesternAspectService(context)
    
    # 1. Native Natal Chart
    natal_chart = chart_service.create_chart(t_birth, request.location.latitude, request.location.longitude)
    
    # 2. Progressed Chart
    prog_chart = progression_service.calculate_secondary_progression(t_birth, t_target)
    
    # 3. Aspects (Progressed to Natal)
    # We compare progressed planets (Points) vs natal planets (Points)
    aspects = aspect_service.calculate_aspects(prog_chart.planets, natal_chart.planets)

    mapped_aspects = [
        TransitAspectSchema(
            p1=a.p1.name,
            p2=a.p2.name,
            aspect_type=a.type,
            orb=a.orb,
            time=t_target.dt
        )
        for a in aspects
    ]

    return TransitScanResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode),
        data=TransitScanData(time=target_date, aspects=mapped_aspects),
    )
