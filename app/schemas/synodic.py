"""Schemas for the /api/v2/synodic endpoints."""
from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class SynodicConjunctionSchema(BaseModel):
    """An exact synodic event (conjunction, opposition, or other angle) between two planets."""

    p1: str
    p2: str
    target_angle: float = Field(..., description="Target angle in degrees (0=Conjunction, 180=Opposition)")
    time: datetime
    julian_day: float


class SynodicConjunctionResponse(BaseAstroResponse[SynodicConjunctionSchema]):
    pass
