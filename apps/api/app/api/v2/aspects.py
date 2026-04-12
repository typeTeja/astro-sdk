from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet, validate_enum_by_name
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.transits import TransitAspectSchema, TransitScanData, TransitScanResponse
from app.services.western import WesternAspectService
from app.services.western.chart_service import WesternChartService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/calculate", response_model=TransitScanResponse, summary="Calculate aspects between objects"
)
def get_aspects(
    time: datetime = Query(...),
    planets: list[str] | None = Query(None),
    aspect_types: list[str] | None = Query(None),
    global_orb: float | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> TransitScanResponse:
    """
    Search for angular interactions (aspects) between planets at a given moment.
    """
    t = Time(time)

    # Resolve planet names to enums
    target_planets = []
    if planets:
        target_planets = [validate_enum_by_name(Planet, p) for p in planets]
    else:
        target_planets = [
            Planet.SUN,
            Planet.MOON,
            Planet.MERCURY,
            Planet.VENUS,
            Planet.MARS,
            Planet.JUPITER,
            Planet.SATURN,
            Planet.URANUS,
            Planet.NEPTUNE,
            Planet.PLUTO,
        ]

    chart_service = WesternChartService(context, ephemeris=ephemeris)
    aspect_service = WesternAspectService(context)

    # 1. Calculate positions
    chart = chart_service.create_chart(t, lat=0, lon=0)

    # Filter chart planets to only requested ones
    planet_objects = [p for p in chart.planets if p.planet in target_planets]

    # 3. Scan
    matches = aspect_service.calculate_aspects(
        planet_objects, aspect_types=aspect_types, global_orb=global_orb
    )

    data = [
        TransitAspectSchema(
            transit_planet=m.p1.name,
            natal_planet=m.p2.name,
            aspect_type=m.type,  # Domain returns 'type', Schema expects 'aspect_type'
            angle=m.angle,
            orb=m.orb,
            is_applying=m.applying,  # Domain returns 'applying', Schema expects 'is_applying'
        )
        for m in matches
    ]

    return TransitScanResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="western.aspects.calculate",
            feature_maturity="PRODUCTION"
        ),
        data=TransitScanData(time=t.dt, aspects=data),
    )
