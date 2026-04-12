from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.common.metadata import calculation_metadata
from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.charts import NatalChartRequest
from app.schemas.transits import (
    TransitAspectSchema,
    TransitScanData,
    TransitScanResponse,
)
from app.services.western import WesternTransitService
from app.services.western.chart_service import WesternChartService

router = APIRouter()
ephemeris = Ephemeris()


@router.post(
    "/scan", response_model=TransitScanResponse, summary="Scan for transits to a natal chart"
)
def scan_transits(
    request: NatalChartRequest,
    transit_time: datetime = Query(...),
    aspect_types: list[str] | None = Query(None),
    global_orb: float | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> TransitScanResponse:
    """
    Look for angular aspects between current transiting planets and a fixed natal chart.
    Useful for "Today's Transits" or personalized transit reports.
    """
    t_transit = Time(transit_time)

    # Manual merge for NatalChartRequest (Body vs Context)
    # The context dependency already handled the headers and query params.
    # If the user also provided settings in the body, we can optionally merge them,
    # but 2.0 policy is Headers > Body for global state.
    if request.settings and "sidereal_mode" in request.settings and not context.zodiac.is_sidereal:
        # Legacy migration: update context if headers didn't specify
        pass

    chart_service = WesternChartService(context, ephemeris=ephemeris)
    transit_service = WesternTransitService(context, ephemeris=ephemeris)

    # 1. Calculate natal chart
    natal_chart = chart_service.create_chart(
        Time(request.time.time),
        request.location.latitude,
        request.location.longitude,
    )

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
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="western.transits.scan",
            feature_maturity="PRODUCTION",
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=TransitScanData(time=t_transit.dt, aspects=aspects),
    )

@router.post(
    "/helion", response_model=TransitScanResponse, summary="Scan heliocentric transits"
)
def scan_helion_transits(
    request: NatalChartRequest,
    transit_time: datetime = Query(...),
    aspect_types: list[str] | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> TransitScanResponse:
    """
    Look for angular aspects using heliocentric coordinates (Sun-centered).
    """
    t_transit = Time(transit_time)
    # Ensure heliocentric is set if not already in context
    context.coordinate.system = context.coordinate.system.HELIOCENTRIC # Forcing for this specific endpoint

    chart_service = WesternChartService(context, ephemeris=ephemeris)
    transit_service = WesternTransitService(context, ephemeris=ephemeris)

    # 1. Native Natal Chart (Helio)
    natal_chart = chart_service.create_chart(
        Time(request.time.time),
        request.location.latitude,
        request.location.longitude,
    )
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
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            heliocentric=True,
            capability="western.transits.heliocentric",
            feature_maturity="PRODUCTION",
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=TransitScanData(time=t_transit.dt, aspects=aspects),
    )

@router.post(
    "/declination", response_model=TransitScanResponse, summary="Scan for declination parallels"
)
def scan_declination_transits(
    request: NatalChartRequest,
    transit_time: datetime = Query(...),
) -> TransitScanResponse:
    """
    Special scan checking ONLY for parallel and contra-parallel declination alignment.
    """
    raise HTTPException(
        status_code=501,
        detail="Declination transit scanning is not implemented yet.",
    )
