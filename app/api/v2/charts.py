from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.common import calculation_metadata
from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import HouseSystem
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.contexts.zodiac import ZodiacType
from app.schemas.astro import PlanetPositionData
from app.schemas.charts import (
    NatalChartData,
    NatalChartRequest,
    NatalChartResponse,
    PanchangaDataSchema,
    PanchangaResponse,
    TransitChartData,
    TransitChartResponse,
)
from app.services.vedic.panchanga_service import VedicPanchangaService
from app.services.western import WesternChartService

router = APIRouter()
ephemeris = Ephemeris()


@router.post("/natal", response_model=NatalChartResponse, summary="Generate full natal chart")
def create_natal_chart(
    request: NatalChartRequest,
    context: CalculationContext = Depends(get_calculation_context)
) -> NatalChartResponse:
    """
    Generate planetary positions, house cusps, and axes for a birth moment.
    """
    t = Time(request.time.time)

    # 2.0 High-Level Priority: Headers > Body Settings
    # If the context didn't get values from headers/query, we fallback to body
    if context.observer is None or (context.observer.latitude == 0.0 and context.observer.longitude == 0.0):
        from app.contexts.observer import ObserverContext
        context.observer = ObserverContext(
            latitude=request.location.latitude,
            longitude=request.location.longitude,
            altitude=request.location.altitude or 0.0
        )

    # 2.0 Mapping: Override Context with ChartSettings payload
    if request.settings:
        if request.settings.house_system:
            context.house.system = request.settings.house_system
        if request.settings.is_sidereal is not None:
            context.zodiac.zodiac = ZodiacType.SIDEREAL if request.settings.is_sidereal else ZodiacType.TROPICAL
        if request.settings.sidereal_mode:
            context.zodiac.sidereal_mode = request.settings.sidereal_mode

    chart_service = WesternChartService(context, ephemeris=ephemeris)
    chart = chart_service.create_chart(
        t,
        request.location.latitude,
        request.location.longitude,
    )
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "time": t.dt.isoformat(),
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "altitude": request.location.altitude,
        },
    )

    planets = [
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
        for p in chart.planets
    ]

    cusps: list[float] = []
    asc = 0.0
    mc = 0.0

    if chart.houses is not None:
        cusps = [c.longitude for c in chart.houses.cusps]
        if chart.houses.axes is not None:
            asc = chart.houses.axes.ascendant
            mc = chart.houses.axes.midheaven

    data = NatalChartData(planets=planets, houses=cusps, ascendant=asc, mc=mc)

    return NatalChartResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            house_system=context.house.system,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=data
    )


@router.get("/transits", response_model=TransitChartResponse, summary="Get current transit chart")
def get_transit_chart(
    time: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> TransitChartResponse:
    """
    Calculate planetary positions for a given moment and location (Transit Chart).
    """
    t = Time(time)
    chart_service = WesternChartService(context, ephemeris=ephemeris)
    chart = chart_service.create_chart(
        t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
    )
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "time": t.dt.isoformat(),
            "latitude": context.observer.latitude if context.observer else 0.0,
            "longitude": context.observer.longitude if context.observer else 0.0,
        },
    )

    planets = [
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
        for p in chart.planets
    ]

    return TransitChartResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            house_system=context.house.system,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=TransitChartData(planets=planets)
    )


@router.get("/panchanga", response_model=PanchangaResponse, summary="Calculate Panchanga")
def get_panchanga(
    time: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> PanchangaResponse:
    """
    Calculate the five elements of the Vedic calendar (Tithi, Nakshatra, Yoga, Karana, Vara).
    """
    t = Time(time)

    pan_service = VedicPanchangaService(context, ephemeris=ephemeris)
    results = pan_service.calculate_panchanga(
        t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0
    )

    data = PanchangaDataSchema(
        tithi=results.tithi,
        nakshatra=results.nakshatra,
        yoga=results.yoga,
        karana=results.karana,
        vara=results.vara,
        sunrise=results.sunrise,
        sunset=results.sunset,
    )

    return PanchangaResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="vedic.panchanga"
        ),
        data=data
    )
