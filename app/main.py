from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .api.v1 import (
    alerts,
    aspects,
    astro,
    charts,
    crossings,
    cycles,
    events,
    financial,
    heliacal,
    horizon,
    lunar,
    nodes,
    parans,
    progressions,
    projections,
    quant,
    research,
    signals,
    stars,
    synodic,
    transits,
    vedic,
)
from .core.database import create_db_and_tables
from .core.errors import (
    AstroError,
    ConfigurationError,
    EphemerisError,
    InvalidTimeError,
    SearchRangeTooLargeError,
    UnsupportedPlanetError,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handle startup and shutdown events.
    Initializes the SQLite database and Swiss Ephemeris.
    """
    create_db_and_tables()
    yield


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AstroSDK Backend Platform",
    description="Professional-grade astronomical research and alert engine.",
    version="1.5.2",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for initial Frontend development and cross-domain VPS usage
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global Exception Handlers
# Maps domain AstroError subclasses to appropriate HTTP status codes.
# ---------------------------------------------------------------------------


@app.exception_handler(UnsupportedPlanetError)
async def unsupported_planet_handler(request: Request, exc: UnsupportedPlanetError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": "unsupported_planet", "detail": str(exc)})


@app.exception_handler(InvalidTimeError)
async def invalid_time_handler(request: Request, exc: InvalidTimeError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": "invalid_time", "detail": str(exc)})


@app.exception_handler(SearchRangeTooLargeError)
async def search_range_handler(request: Request, exc: SearchRangeTooLargeError) -> JSONResponse:
    return JSONResponse(
        status_code=400, content={"error": "search_range_too_large", "detail": str(exc)}
    )


@app.exception_handler(ConfigurationError)
async def configuration_handler(request: Request, exc: ConfigurationError) -> JSONResponse:
    return JSONResponse(
        status_code=503, content={"error": "configuration_error", "detail": str(exc)}
    )


@app.exception_handler(EphemerisError)
async def ephemeris_handler(request: Request, exc: EphemerisError) -> JSONResponse:
    return JSONResponse(
        status_code=500, content={"error": "ephemeris_error", "detail": str(exc)}
    )


@app.exception_handler(AstroError)
async def generic_astro_handler(request: Request, exc: AstroError) -> JSONResponse:
    """Catch-all for any AstroError subclass not matched above."""
    return JSONResponse(
        status_code=500, content={"error": "astro_error", "detail": str(exc)}
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

# Core data routers
app.include_router(astro.router, prefix="/api/v1/astro", tags=["Astro"])
app.include_router(charts.router, prefix="/api/v1/charts", tags=["Charts"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(lunar.router, prefix="/api/v1/lunar", tags=["Lunar"])
app.include_router(aspects.router, prefix="/api/v1/aspects", tags=["Aspects"])
app.include_router(progressions.router, prefix="/api/v1/progressions", tags=["Progressions"])
app.include_router(quant.router, prefix="/api/v1/quant", tags=["Quantitative"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(vedic.router, prefix="/api/v1/vedic", tags=["Vedic"])
app.include_router(transits.router, prefix="/api/v1/transits", tags=["Transits"])

# Newly added routers (Phase 3 & Phase 4)
app.include_router(crossings.router, prefix="/api/v1/crossings", tags=["Crossings"])
app.include_router(horizon.router, prefix="/api/v1/horizon", tags=["Horizon"])
app.include_router(stars.router, prefix="/api/v1/stars", tags=["Fixed Stars"])
app.include_router(nodes.router, prefix="/api/v1/nodes", tags=["Nodes & Apsides"])
app.include_router(parans.router, prefix="/api/v1/parans", tags=["Parans"])
app.include_router(heliacal.router, prefix="/api/v1/heliacal", tags=["Heliacal"])
app.include_router(synodic.router, prefix="/api/v1/synodic", tags=["Synodic"])
app.include_router(financial.router, prefix="/api/v1/financial", tags=["Financial Astrology"])
app.include_router(signals.router, prefix="/api/v1/signals", tags=["Signals & Statistical"])
app.include_router(research.router, prefix="/api/v1/research", tags=["Research & Export"])
app.include_router(cycles.router, prefix="/api/v1/cycles", tags=["Cycles & Composite"])
app.include_router(projections.router, prefix="/api/v1/projections", tags=["Mathematical Projections"])

@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """
    Health check endpoint.
    """
    return {"message": "AstroSDK Backend Platform is Online", "status": "ok"}

@app.get("/version", tags=["Health"])
async def version() -> dict[str, str]:
    """
    Platform version check.
    """
    return {"version": "1.5.2"}
