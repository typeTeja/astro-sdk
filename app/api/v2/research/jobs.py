"""
/api/v2/research — Heavy data aggregation endpoints meant for integration
into pandas, ML analytics, and other external bulk research programs.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.core.constants import SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.services.research.export_service import ResearchExportService
from app.contexts.factories import create_default_context
from app.api.v2.meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/ephemeris/csv",
    summary="Stream bulk ephemeris data as CSV",
    response_class=StreamingResponse,
    description="Warning: Highly processor intensive. Do not set span > 5 years without caution.",
)
async def get_ephemeris_csv(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    years: float = Query(1.0, gt=0, le=5.0, description="Range to cover in years (Max 5)"),
    step_hours: float = Query(24.0, ge=1.0, le=720.0, description="Sampling rate"),
    is_sidereal: bool = Query(True),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> StreamingResponse:
    """
    Downloads raw structured astronomical data for data scientists.
    Uses StreamingResponse to yield chunks without buffering into RAM.
    """
    if years > 5.0:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Max 5 years allowed per request.")
        
    t_start = Time(start_time)
    t_end = Time.from_julian_day(t_start.julian_day + (years * 365.25))

    context = create_default_context()
    context.zodiac.is_sidereal = is_sidereal
    context.zodiac.sidereal_mode = sidereal_mode
    
    export_service = ResearchExportService(context, ephemeris=ephemeris)
    from app.core.constants import Planet
    planets = [Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS, Planet.MARS, Planet.JUPITER, Planet.SATURN]
    
    from datetime import timedelta
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

from app.schemas.research import ResearchAnalyticsData, ResearchAnalyticsResponse, ScanRequestSchema

@router.post("/astro-scan", response_model=ResearchAnalyticsResponse)
async def post_astro_scan(
    request: ScanRequestSchema,
) -> ResearchAnalyticsResponse:
    # Stubbed analytical map
    data = ResearchAnalyticsData(count=0, results=[], summary={"scan_type": "angle_target"})
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)

@router.get("/astro-events", response_model=ResearchAnalyticsResponse)
async def get_astro_events(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    end_time: datetime | None = Query(None),
) -> ResearchAnalyticsResponse:
    # Blanket list of AstroEvent
    data = ResearchAnalyticsData(count=0, results=[])
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)

@router.get("/event-frequency", response_model=ResearchAnalyticsResponse)
async def get_event_frequency(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    end_time: datetime | None = Query(None),
) -> ResearchAnalyticsResponse:
    # Map frequency counts
    data = ResearchAnalyticsData(count=0, results=[], summary={"mode": "frequency"})
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)

@router.get("/astro-dataset", response_model=ResearchAnalyticsResponse)
async def get_astro_dataset(
    start_time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> ResearchAnalyticsResponse:
    # Top-level dataset definition
    data = ResearchAnalyticsData(count=1, results=[{"dataset_type": "compiled"}])
    return ResearchAnalyticsResponse(meta=get_meta(), data=data)
