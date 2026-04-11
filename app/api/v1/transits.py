from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...engine.chart_engine import ChartEngine
from ...schemas.charts import NatalChartRequest
from ...schemas.transits import TransitAspectSchema, TransitScanData, TransitScanResponse
from ...services.western import WesternTransitService
from ..common import build_western_chart_context, calculation_metadata
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
chart_engine = ChartEngine()


@router.post(
    "/scan", response_model=TransitScanResponse, summary="Scan for transits to a natal chart"
)
async def scan_transits(
    request: NatalChartRequest,
    transit_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    aspect_types: list[str] | None = Query(None),
    global_orb: float | None = Query(None),
) -> TransitScanResponse:
    """
    Look for angular aspects between current transiting planets and a fixed natal chart.
    Useful for "Today's Transits" or personalized transit reports.
    """
    t_transit = Time(transit_time)

    # Resolve settings with defaults
    sidereal_mode = SiderealMode.LAHIRI
    is_sidereal = True
    if request.settings:
        if "sidereal_mode" in request.settings:
            sidereal_mode = SiderealMode(request.settings["sidereal_mode"])
        if "is_sidereal" in request.settings:
            is_sidereal = bool(request.settings["is_sidereal"])

    # 1. Calculate natal chart from birth data
    natal_chart = chart_engine.create_chart(
        Time(request.time.time),
        request.location.latitude,
        request.location.longitude,
        sidereal_mode=sidereal_mode,
    )

    context = build_western_chart_context(
        sidereal_mode=sidereal_mode,
        is_sidereal=is_sidereal,
        heliocentric=False,
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        altitude=request.location.altitude,
        capability="western.transit",
    )
    transit_service = WesternTransitService(context, ephemeris=ephemeris)

    # 2. Run transit scan — returns domain TransitAspect objects
    domain_aspects = transit_service.scan_transits(
        natal_chart.planets,
        t_transit,
        aspect_types=aspect_types,
        global_orb=global_orb,
    )
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "birth_time": request.time.time.isoformat(),
            "transit_time": t_transit.dt.isoformat(),
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "aspect_types": aspect_types or [],
            "global_orb": global_orb,
        },
    )

    # 4. Map domain TransitAspect → TransitAspectSchema (schema layer responsibility)
    aspects = [
        TransitAspectSchema(
            transit_planet=a.transit_planet.name,
            natal_planet=a.natal_planet,
            aspect_type=a.aspect_type,
            angle=a.angle,
            orb=a.orb,
            is_applying=a.is_applying,
        )
        for a in domain_aspects
    ]

    return TransitScanResponse(
        meta=get_meta(
            is_sidereal=is_sidereal,
            sidereal_mode=sidereal_mode,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=TransitScanData(time=t_transit.dt, aspects=aspects),
    )

@router.post(
    "/helion", response_model=TransitScanResponse, summary="Scan heliocentric transits"
)
async def scan_helion_transits(
    request: NatalChartRequest,
    transit_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    aspect_types: list[str] | None = Query(None),
) -> TransitScanResponse:
    """
    Look for angular aspects using heliocentric coordinates (Sun-centered).
    """
    t_transit = Time(transit_time)
    natal_chart = chart_engine.create_chart(
        Time(request.time.time),
        request.location.latitude,
        request.location.longitude,
        is_sidereal=False,
        heliocentric=True,
    )
    context = build_western_chart_context(
        is_sidereal=False,
        heliocentric=True,
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        altitude=request.location.altitude,
        capability="western.transit.helio",
    )
    transit_service = WesternTransitService(context, ephemeris=ephemeris)
    domain_aspects = transit_service.scan_transits(
        natal_chart.planets,
        t_transit,
        aspect_types=aspect_types,
    )
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "birth_time": request.time.time.isoformat(),
            "transit_time": t_transit.dt.isoformat(),
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "aspect_types": aspect_types or [],
        },
    )
    aspects = [TransitAspectSchema(transit_planet=a.transit_planet.name, natal_planet=a.natal_planet, aspect_type=a.aspect_type, angle=a.angle, orb=a.orb, is_applying=a.is_applying) for a in domain_aspects]
    return TransitScanResponse(
        meta=get_meta(
            is_sidereal=False,
            sidereal_mode=None,
            heliocentric=True,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=TransitScanData(time=t_transit.dt, aspects=aspects),
    )

@router.post(
    "/declination", response_model=TransitScanResponse, summary="Scan for declination parallels"
)
async def scan_declination_transits(
    request: NatalChartRequest,
    transit_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> TransitScanResponse:
    """
    Special scan checking ONLY for parallel and contra-parallel declination alignment.
    """
    raise HTTPException(
        status_code=501,
        detail="Declination transit scanning is not implemented yet.",
    )
