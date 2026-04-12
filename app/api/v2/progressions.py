from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.astro import PlanetPositionData
from app.schemas.charts import NatalChartRequest
from app.schemas.transits import (
    SecondaryProgressionData,
    SecondaryProgressionResponse,
    TransitAspectSchema,
    TransitScanData,
    TransitScanResponse,
)
from app.services.western import WesternProgressionService
from app.services.western.aspect_service import WesternAspectService
from app.services.western.chart_service import WesternChartService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/secondary",
    response_model=SecondaryProgressionResponse,
    summary="Get secondary progression positions",
)
def get_secondary_progression(
    birth_time: datetime = Query(...),
    target_date: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> SecondaryProgressionResponse:
    """
    Calculate Secondary Progressions (Day-for-a-Year) for a given life moment.
    """
    t_birth = Time(birth_time)
    t_target = Time(target_date)
    progression_service = WesternProgressionService(context, ephemeris=ephemeris)

    # 1. Calculate progressions → returns ProgressedChart domain object
    prog = progression_service.calculate_secondary_progression(t_birth, t_target)

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
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="western.progression"
        ),
        data=data
    )




@router.post(
    "/aspects",
    response_model=TransitScanResponse,
    summary="Scan valid aspects between progressed planets and natal chart",
)
def get_progression_aspects(
    request: NatalChartRequest,
    target_date: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> TransitScanResponse:
    """
    Scans the progressed state against the natal chart structure.
    Returns domain transit aspects mapping progressed planets.
    """
    t_birth = Time(request.time.time)
    t_target = Time(target_date)

    chart_service = WesternChartService(context, ephemeris=ephemeris)
    progression_service = WesternProgressionService(context, ephemeris=ephemeris)
    aspect_service = WesternAspectService(context)

    # 1. Native Natal Chart
    natal_chart = chart_service.create_chart(t_birth, request.location.latitude, request.location.longitude)

    # 2. Progressed Chart
    prog_chart = progression_service.calculate_secondary_progression(t_birth, t_target)

    # 3. Aspects (Progressed to Natal)
    # Use points_b for synastry-style comparison
    aspects = aspect_service.calculate_aspects(list(prog_chart.planets), points_b=list(natal_chart.planets))

    mapped_aspects = [
        TransitAspectSchema(
            transit_planet=a.p1.name,
            natal_planet=a.p2.name,
            aspect_type=a.type,
            angle=a.angle,
            orb=a.orb,
            is_applying=a.applying
        )
        for a in aspects
    ]

    return TransitScanResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="western.progression.aspects"
        ),
        data=TransitScanData(time=target_date, aspects=mapped_aspects)
    )
