from datetime import UTC, datetime

from fastapi import APIRouter, Query

from app.core.constants import SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.contexts import FeatureMaturity
from app.schemas.astro import PlanetPositionData
from app.schemas.charts import NatalChartRequest
from app.schemas.transits import SecondaryProgressionData, SecondaryProgressionResponse
from app.services.western import WesternProgressionService
from app.services.western.chart_service import WesternChartService
from app.services.western.aspect_service import WesternAspectService
from app.contexts.factories import create_default_context, build_western_chart_context
from app.api.common.metadata import calculation_metadata
from app.api.v2.meta import get_meta

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

    # 2. Map domain objects → PlanetPositionData schemas (schema layer)
    planets_data = [
        PlanetPositionData(
            planet=p.planet.name,
            longitude=p.longitude,
            latitude=p.latitude,
            distance=p.distance,
            speed_long=p.speed_long,
            is_retrograde=p.is_retrograde,
            sign=p.sign,
            sign_name=p.sign_name,
        )
        for p in prog.planets
    ]

    data = SecondaryProgressionData(
        progression_date=prog.progressed_time,
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

from app.schemas.transits import TransitScanResponse, TransitScanData, TransitAspectSchema

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
