from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import HouseSystem, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.astro import PlanetPositionData
from ...schemas.charts import (
    NatalChartData,
    NatalChartRequest,
    NatalChartResponse,
    PanchangaData,
    PanchangaResponse,
    TransitChartData,
    TransitChartResponse,
)
from ...engine.chart_engine import ChartEngine
from ...services.panchanga_service import PanchangaService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
chart_engine = ChartEngine()
pan_service = PanchangaService(ephemeris)


@router.post("/natal", response_model=NatalChartResponse, summary="Generate full natal chart")
async def create_natal_chart(request: NatalChartRequest) -> NatalChartResponse:
    """
    Generate planetary positions, house cusps, and axes for a birth moment.
    """
    t = Time(request.time.time)

    # Resolve settings with defaults
    house_sys = HouseSystem.PLACIDUS
    sidereal_mode = SiderealMode.LAHIRI
    is_sidereal = True

    if request.settings:
        if "house_system" in request.settings:
            house_sys = HouseSystem(request.settings["house_system"])
        if "sidereal_mode" in request.settings:
            sidereal_mode = SiderealMode(request.settings["sidereal_mode"])
        if "is_sidereal" in request.settings:
            is_sidereal = bool(request.settings["is_sidereal"])

    chart = chart_engine.create_chart(
        t,
        request.location.latitude,
        request.location.longitude,
        system=house_sys,
        sidereal_mode=sidereal_mode,
        is_sidereal=is_sidereal,
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
        meta=get_meta(is_sidereal=is_sidereal, sidereal_mode=sidereal_mode), data=data
    )


@router.get("/transits", response_model=TransitChartResponse, summary="Get current transit chart")
async def get_transit_chart(
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    latitude: float = Query(0.0),
    longitude: float = Query(0.0),
    sidereal: bool = Query(True),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> TransitChartResponse:
    """
    Calculate planetary positions for a given moment and location (Transit Chart).
    """
    t = Time(time)

    chart = chart_engine.create_chart(
        t,
        latitude,
        longitude,
        system=HouseSystem.PLACIDUS,
        sidereal_mode=sidereal_mode,
        is_sidereal=sidereal,
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
        meta=get_meta(is_sidereal=sidereal, sidereal_mode=sidereal_mode),
        data=TransitChartData(planets=planets),
    )


@router.get("/panchanga", response_model=PanchangaResponse, summary="Calculate Panchanga")
async def get_panchanga(
    latitude: float = Query(...),
    longitude: float = Query(...),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> PanchangaResponse:
    """
    Calculate the five elements of the Vedic calendar (Tithi, Nakshatra, Yoga, Karana, Vara).
    """
    t = Time(time)
    results = pan_service.calculate_panchanga(t, latitude, longitude)

    data = PanchangaData(
        tithi=results.tithi,
        nakshatra=results.nakshatra,
        yoga=results.yoga,
        karana=results.karana,
        vara=results.vara,
        sunrise=results.sunrise,
        sunset=results.sunset,
    )

    return PanchangaResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=SiderealMode.LAHIRI), data=data
    )
