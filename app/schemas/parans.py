"""Schemas for the /api/v2/parans endpoints."""
from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class ParanSchema(BaseModel):
    """A paran — simultaneous horizon/meridian event between two bodies."""

    p1: str = Field(..., description="First planet")
    event1: str = Field(..., description="Rise, Set, Transit, or IC for p1")
    p2: str = Field(..., description="Second planet")
    event2: str = Field(..., description="Rise, Set, Transit, or IC for p2")
    time: datetime = Field(..., description="Midpoint time of the paran")
    orb_minutes: float = Field(..., description="Angular separation in minutes of arc")


class ParanResponse(BaseAstroResponse[list[ParanSchema]]):
    pass
