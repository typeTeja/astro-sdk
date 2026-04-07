from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.charts import NatalChartRequest
from ...schemas.transits import TransitScanData, TransitScanResponse
from ...services.transit_service import TransitService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
transit_service = TransitService(ephemeris)


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

    # 1. Prepare natal positions as PlanetPositionData (the service expects this)
    # The request has raw natal data, but we need to calculate it or use provided.
    # For now, we assume the request provides a location to calculate from.
    from ...services.chart_engine import ChartEngine

    engine = ChartEngine(ephemeris)
    natal_chart = engine.create_chart(
        Time(request.time.time),
        request.location.latitude,
        request.location.longitude,
        sidereal_mode=sidereal_mode,
    )

    # Map domain positions to schema data
    from ...schemas.astro import PlanetPositionData

    natal_data = [
        PlanetPositionData(
            planet=p.planet.name,
            longitude=p.longitude,
            latitude=p.latitude,
            distance=p.distance,
            speed_long=p.speed_long,
            is_retrograde=p.is_retrograde,
            sign=p.sign,
            sign_name=PlanetPositionData.get_sign_name(p.longitude),
        )
        for p in natal_chart.planets
    ]

    # 2. Run scan
    aspects = transit_service.calculate_transit_aspects(
        natal_data,
        t_transit,
        sidereal_mode=sidereal_mode,
        aspect_types=aspect_types,
        global_orb=global_orb,
    )

    return TransitScanResponse(
        meta=get_meta(is_sidereal=is_sidereal, sidereal_mode=sidereal_mode),
        data=TransitScanData(time=t_transit.dt, aspects=aspects),
    )
