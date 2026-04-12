"""Schemas for the /api/v2/stars endpoints."""
from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class FixedStarSchema(BaseModel):
    """Position and brightness of a fixed star."""

    name: str
    longitude: float = Field(..., description="Ecliptic longitude in degrees (0–360)")
    latitude: float = Field(..., description="Ecliptic latitude in degrees")
    magnitude: float = Field(..., description="Visual magnitude (lower = brighter)")


class FixedStarResponse(BaseAstroResponse[FixedStarSchema]):
    pass


class FixedStarsListResponse(BaseAstroResponse[list[FixedStarSchema]]):
    pass
