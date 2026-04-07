from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .base import BaseAstroResponse


class ResearchAnalyticsData(BaseModel):
    """Generic wrapper for JSON analytical data."""

    count: int
    results: list[dict[str, Any]]
    summary: dict[str, Any] | None = None


class ResearchAnalyticsResponse(BaseAstroResponse[ResearchAnalyticsData]):
    pass


class ScanRequestSchema(BaseModel):
    """Schema for requesting a complex astro-scan."""

    planets: list[str]
    start_time: datetime
    end_time: datetime
    target_angle: float | None = None
