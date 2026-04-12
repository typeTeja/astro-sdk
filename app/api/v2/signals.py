"""
/api/v2/signals — Macro-level quantitative metrics on the sky state.

Non-predictive tracking of system energy density (number of active aspects)
and planetary clustering (Stelliums).
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.signals import (
    AstroIntensityList,
    AstroIntensityResponse,
    AstroIntensitySchema,
    ClusterIndexResponse,
    ClusterIndexSchema,
    ClusterSchema,
)
from app.services.research.quant_service import ResearchQuantService
from app.contexts.factories import create_default_context
from app.api.v2.meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/astro-intensity",
    response_model=AstroIntensityResponse,
    summary="Get rolling aspect intensity scores",
)
async def get_astro_intensity(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    max_days: float = Query(30.0, gt=0, le=365.0),
    step_hours: int = Query(24, ge=1, le=168),
) -> AstroIntensityResponse:
    """
    Returns a time-series scoring the "intensity" of the sky.
    Higher scores indicate more active exact major planetary aspects.
    """
    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + max_days)
    
    context = create_default_context()
    signals_service = ResearchQuantService(context, ephemeris=ephemeris)

    results = signals_service.calculate_intensity(t_start, t_end, step_hours)

    schemas = [
        AstroIntensitySchema(
            time=r.time,
            score=r.score,
            active_aspects_count=r.active_aspects_count,
            top_contributors=r.top_contributors,
        )
        for r in results
    ]

    return AstroIntensityResponse(
        meta=get_meta(is_sidereal=False, sidereal_mode=None),
        data=AstroIntensityList(intensities=schemas),
    )


@router.get(
    "/cluster-index",
    response_model=ClusterIndexResponse,
    summary="Find planetary clusters (Stelliums)",
)
async def get_cluster_index(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    max_days: float = Query(30.0, gt=0, le=365.0),
    step_hours: int = Query(24, ge=1, le=168),
    orb_degrees: float = Query(10.0, ge=1.0, le=30.0),
) -> ClusterIndexResponse:
    """
    Maps dense clusters of 3+ planets grouped within a tight orb.
    """
    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + max_days)
    
    context = create_default_context()
    signals_service = ResearchQuantService(context, ephemeris=ephemeris)

    results = signals_service.calculate_cluster_index(t_start, t_end, orb_degrees, step_hours)

    schemas = [
        ClusterIndexSchema(
            time=r.time,
            stellar_density_score=r.stellar_density_score,
            clusters=[
                ClusterSchema(
                    center_longitude=c.center_longitude,
                    span_degrees=c.span_degrees,
                    planets=c.planets,
                )
                for c in r.clusters
            ],
        )
        for r in results
    ]

    return ClusterIndexResponse(
        meta=get_meta(is_sidereal=False, sidereal_mode=None),
        data=schemas,
    )
