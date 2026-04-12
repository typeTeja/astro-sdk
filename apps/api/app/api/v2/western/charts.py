from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.contexts.calculation import CalculationContext
from app.core.time import Time
from app.schemas.charts import NatalChartRequest, NatalChartResponse, TransitChartResponse
from app.services.western.chart_service import WesternChartService

router = APIRouter()


@router.post("/natal", response_model=NatalChartResponse, summary="[V2] Generate full natal chart")
def create_natal_chart(
    request: NatalChartRequest,
    context: Annotated[CalculationContext, Depends(get_calculation_context)]
) -> NatalChartResponse:
    """
    Generate planetary positions and house cursps using the 2.0 Native Engine.
    """
    t = Time(request.time.time)

    # Ensure location is reflected in context for house calculation
    if not context.observer:
        from app.contexts.observer import ObserverContext
        context.observer = ObserverContext(
            latitude=request.location.latitude,
            longitude=request.location.longitude,
            altitude=request.location.altitude
        )
    else:
        context.observer = context.observer.model_copy(update={
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "altitude": request.location.altitude
        })

    service = WesternChartService(context)
    chart = service.create_chart(t, context.observer.latitude, context.observer.longitude)

    # Map to NatalChartData schema
    from app.api.v2.meta import get_meta
    from app.schemas.astro import PlanetPositionData
    from app.schemas.charts import NatalChartData

    planets = [
        PlanetPositionData(
            planet=p.planet.name,
            longitude=p.longitude,
            latitude=p.latitude,
            distance=p.distance,
            speed_long=p.speed_long,
            is_retrograde=p.is_retrograde,
            sign=p.sign + 1,
            sign_name=PlanetPositionData.get_sign_name(p.longitude)
        ) for p in chart.planets
    ]

    cusps = [c.longitude for c in chart.houses.cusps] if chart.houses else []
    asc = chart.houses.axes.ascendant if chart.houses and chart.houses.axes else 0.0
    mc = chart.houses.axes.midheaven if chart.houses and chart.houses.axes else 0.0

    data = NatalChartData(planets=planets, houses=cusps, ascendant=asc, mc=mc)

    return NatalChartResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.zodiac == "sidereal",
            sidereal_mode=context.zodiac.sidereal_mode,
            house_system=context.house.system,
            capability="western.natal",
            feature_maturity=context.feature.maturity.value,
            calculation_fingerprint=context.fingerprint
        ),
        data=data
    )


@router.get("/transits", response_model=TransitChartResponse, summary="[V2] Get transit chart")
def get_transit_chart(
    context: Annotated[CalculationContext, Depends(get_calculation_context)],
    time: datetime = Query(...),
    latitude: float = Query(0.0),
    longitude: float = Query(0.0),
) -> TransitChartResponse:
    """
    Calculate high-precision transits using the 2.0 platform.
    """
    t = Time(time)
    service = WesternChartService(context)
    chart = service.create_chart(t, latitude, longitude)

    from app.api.v2.meta import get_meta
    from app.schemas.astro import PlanetPositionData
    from app.schemas.charts import TransitChartData

    planets = [
        PlanetPositionData(
            planet=p.planet.name,
            longitude=p.longitude,
            latitude=p.latitude,
            distance=p.distance,
            speed_long=p.speed_long,
            is_retrograde=p.is_retrograde,
            sign=p.sign + 1,
            sign_name=PlanetPositionData.get_sign_name(p.longitude)
        ) for p in chart.planets
    ]

    return TransitChartResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.zodiac == "sidereal",
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="western.transit",
            feature_maturity=context.feature.maturity.value,
            calculation_fingerprint=context.fingerprint
        ),
        data=TransitChartData(planets=planets)
    )
