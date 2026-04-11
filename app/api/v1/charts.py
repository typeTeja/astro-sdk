from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...api.common import build_western_chart_context, calculation_metadata
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
from ...services.panchanga_service import PanchangaService
from ...services.western import WesternChartService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
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
    heliocentric = False

    if request.settings:
        if "house_system" in request.settings:
            house_sys = HouseSystem(request.settings["house_system"])
        if "sidereal_mode" in request.settings:
            sidereal_mode = SiderealMode(request.settings["sidereal_mode"])
        if "is_sidereal" in request.settings:
            is_sidereal = bool(request.settings["is_sidereal"])
        if "heliocentric" in request.settings:
            heliocentric = bool(request.settings["heliocentric"])

    context = build_western_chart_context(
        house_system=house_sys,
        sidereal_mode=sidereal_mode,
        is_sidereal=is_sidereal,
        heliocentric=heliocentric,
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        altitude=request.location.altitude,
    )
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
            is_sidereal=is_sidereal,
            sidereal_mode=sidereal_mode,
            heliocentric=heliocentric,
            house_system=house_sys,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=data,
    )


@router.get("/transits", response_model=TransitChartResponse, summary="Get current transit chart")
async def get_transit_chart(
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    latitude: float = Query(0.0),
    longitude: float = Query(0.0),
    sidereal: bool = Query(True),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
    heliocentric: bool = Query(False),
) -> TransitChartResponse:
    """
    Calculate planetary positions for a given moment and location (Transit Chart).
    """
    t = Time(time)

    context = build_western_chart_context(
        house_system=HouseSystem.PLACIDUS,
        sidereal_mode=sidereal_mode,
        is_sidereal=sidereal,
        heliocentric=heliocentric,
        latitude=latitude,
        longitude=longitude,
    )
    chart_service = WesternChartService(context, ephemeris=ephemeris)
    chart = chart_service.create_chart(
        t,
        latitude,
        longitude,
    )
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "time": t.dt.isoformat(),
            "latitude": latitude,
            "longitude": longitude,
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
            is_sidereal=sidereal,
            sidereal_mode=sidereal_mode,
            heliocentric=heliocentric,
            house_system=HouseSystem.PLACIDUS,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
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
