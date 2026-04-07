from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.v1 import (
    alerts,
    aspects,
    astro,
    charts,
    events,
    lunar,
    progressions,
    quant,
    vedic,
)
from .core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handle startup and shutdown events.
    Initializes the SQLite database and Swiss Ephemeris.
    """
    create_db_and_tables()
    yield


app = FastAPI(
    title="AstroSDK Backend Platform",
    description="Professional-grade astronomical research and alert engine.",
    version="1.0.0",
    lifespan=lifespan,
)

# Include Routers
app.include_router(astro.router, prefix="/api/v1/astro", tags=["Astro"])
app.include_router(charts.router, prefix="/api/v1/charts", tags=["Charts"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(lunar.router, prefix="/api/v1/lunar", tags=["Lunar"])
app.include_router(aspects.router, prefix="/api/v1/aspects", tags=["Aspects"])
app.include_router(progressions.router, prefix="/api/v1/progressions", tags=["Progressions"])
app.include_router(quant.router, prefix="/api/v1/quant", tags=["Quantitative"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(vedic.router, prefix="/api/v1/vedic", tags=["Vedic"])


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """
    Health check endpoint.
    """
    return {"message": "AstroSDK Backend Platform is Online", "status": "ok"}
