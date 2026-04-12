from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v2 import (
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
    signals,
    stars,
    synodic,
    transits,
)
from app.api.v2.alerts.rules import router as alert_v2_router
from app.api.v2.astronomy.positions import router as astronomy_v2_router
from app.api.v2.research.jobs import router as research_v2_router
from app.api.v2.vedic.classic import router as vedic_classic_router
from app.api.v2.vedic.panchang import router as vedic_panchang_router
from app.api.v2.western.charts import router as western_v2_router
from app.core.database import create_db_and_tables
from app.core.errors import (
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



app = FastAPI(
    title="AstroSDK 2.0 Platform",
    description="Professional-grade astronomical research and alert engine.",
    version="2.0.0",
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

# ---------------------------------------------------------------------------
# API V2 Routers
# ---------------------------------------------------------------------------

# Domain Specific Routers (Single Module)
app.include_router(astro.router, prefix="/api/v2/astro", tags=["Astro"])
app.include_router(charts.router, prefix="/api/v2/charts", tags=["Charts"])
app.include_router(events.router, prefix="/api/v2/events", tags=["Events"])
app.include_router(lunar.router, prefix="/api/v2/lunar", tags=["Lunar"])
app.include_router(aspects.router, prefix="/api/v2/aspects", tags=["Aspects"])
app.include_router(progressions.router, prefix="/api/v2/progressions", tags=["Progressions"])
app.include_router(quant.router, prefix="/api/v2/quant", tags=["Quantitative"])
app.include_router(transits.router, prefix="/api/v2/transits", tags=["Transits"])
app.include_router(crossings.router, prefix="/api/v2/crossings", tags=["Crossings"])
app.include_router(horizon.router, prefix="/api/v2/horizon", tags=["Horizon"])
app.include_router(stars.router, prefix="/api/v2/stars", tags=["Fixed Stars"])
app.include_router(nodes.router, prefix="/api/v2/nodes", tags=["Nodes & Apsides"])
app.include_router(parans.router, prefix="/api/v2/parans", tags=["Parans"])
app.include_router(heliacal.router, prefix="/api/v2/heliacal", tags=["Heliacal"])
app.include_router(synodic.router, prefix="/api/v2/synodic", tags=["Synodic"])
app.include_router(financial.router, prefix="/api/v2/financial", tags=["Financial Astrology"])
app.include_router(signals.router, prefix="/api/v2/signals", tags=["Signals & Statistical"])
app.include_router(cycles.router, prefix="/api/v2/cycles", tags=["Cycles & Composite"])
app.include_router(projections.router, prefix="/api/v2/projections", tags=["Mathematical Projections"])

# Namespaced Package Routers
app.include_router(astronomy_v2_router, prefix="/api/v2/astronomy", tags=["V2 Astronomy"])
app.include_router(western_v2_router, prefix="/api/v2/western", tags=["V2 Western"])
app.include_router(vedic_panchang_router, prefix="/api/v2/vedic", tags=["V2 Vedic Panchang"])
app.include_router(vedic_classic_router, prefix="/api/v2/vedic/classic", tags=["V2 Vedic Classic"])
app.include_router(research_v2_router, prefix="/api/v2/research", tags=["V2 Research"])
app.include_router(alert_v2_router, prefix="/api/v2/alerts", tags=["V2 Alerts"])


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """
    Health check endpoint.
    """
    return {"message": "AstroSDK 2.0 Platform is Online", "status": "ok"}

@app.get("/version", tags=["Health"])
async def version() -> dict[str, str]:
    """
    Platform version check.
    """
    return {"version": "2.0.0"}
