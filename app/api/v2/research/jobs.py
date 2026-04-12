"""
/api/v2/research — Heavy data aggregation endpoints meant for integration
into pandas, ML analytics, and other external bulk research programs.
"""
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.research import (
    ResearchAnalyticsData,
    ResearchAnalyticsResponse,
    ScanRequestSchema,
)
from app.services.research.export_service import ResearchExportService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/ephemeris/csv",
    summary="Stream bulk ephemeris data as CSV",
    response_class=StreamingResponse,
    description="Warning: Highly processor intensive. Do not set span > 5 years without caution.",
)
def get_ephemeris_csv(
    start_time: datetime = Query(...),
    years: float = Query(1.0, gt=0, le=5.0, description="Range to cover in years (Max 5)"),
    step_hours: float = Query(24.0, ge=1.0, le=720.0, description="Sampling rate"),
    context: CalculationContext = Depends(get_calculation_context),
) -> StreamingResponse:
    """
    Downloads raw structured astronomical data for data scientists.
    Uses StreamingResponse to yield chunks without buffering into RAM.
    """
    if years > 5.0:

        raise HTTPException(status_code=400, detail="Max 5 years allowed per request.")

    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + (years * 365.25))

    export_service = ResearchExportService(context, ephemeris=ephemeris)

    planets = [Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS, Planet.MARS, Planet.JUPITER, Planet.SATURN]


    generator = export_service.stream_ephemeris(
        planets=planets,
        start_time=t_start,
        end_time=t_end,
        step=timedelta(hours=step_hours),
        format="CSV"
    )

    filename = f"ephemeris_{t_start.dt.strftime('%Y%m%d')}_to_{t_end.dt.strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        generator,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )




@router.post("/astro-scan", response_model=ResearchAnalyticsResponse)
def post_astro_scan(
    request: ScanRequestSchema,
) -> ResearchAnalyticsResponse:
    # Stubbed analytical map
    data = ResearchAnalyticsData(count=0, results=[], summary={"scan_type": "angle_target"})
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)

@router.get("/astro-events", response_model=ResearchAnalyticsResponse)
def get_astro_events(
    start_time: datetime = Query(...),
    end_time: datetime | None = Query(None),
) -> ResearchAnalyticsResponse:
    # Blanket list of AstroEvent
    data = ResearchAnalyticsData(count=0, results=[])
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)

@router.get("/event-frequency", response_model=ResearchAnalyticsResponse)
def get_event_frequency(
    start_time: datetime = Query(...),
    end_time: datetime | None = Query(None),
) -> ResearchAnalyticsResponse:
    # Map frequency counts
    data = ResearchAnalyticsData(count=0, results=[], summary={"mode": "frequency"})
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)

@router.get("/astro-dataset", response_model=ResearchAnalyticsResponse)
def get_astro_dataset(
    start_time: datetime = Query(...),
) -> ResearchAnalyticsResponse:
    # Top-level dataset definition
    data = ResearchAnalyticsData(count=1, results=[{"dataset_type": "compiled"}])
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)
