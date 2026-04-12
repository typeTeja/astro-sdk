"""Schemas for the /api/v2/crossings endpoints."""
from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class PlanetaryReturnSchema(BaseModel):
    """A planetary return — when a planet returns to its natal longitude."""

    planet: str
    return_time: datetime
    longitude: float = Field(..., description="The natal longitude reached")


class PlanetaryReturnResponse(BaseAstroResponse[list[PlanetaryReturnSchema]]):
    pass


class AspectCrossingSchema(BaseModel):
    """Exact moment a specific inter-planetary angle is achieved."""

    p1: str
    p2: str
    target_angle: float
    crossing_time: datetime


class AspectCrossingResponse(BaseAstroResponse[list[AspectCrossingSchema]]):
    pass
