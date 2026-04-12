"""Schemas for the /api/v2/heliacal endpoints."""
from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class HeliacalEventSchema(BaseModel):
    """A heliacal or acronychal event."""

    planet: str
    event_type: str = Field(..., description="HELIACAL_RISING, HELIACAL_SETTING, etc.")
    time: datetime | None = Field(None, description="UTC time of the event")


class HeliacalResponse(BaseAstroResponse[HeliacalEventSchema]):
    pass


class StationSchema(BaseModel):
    """A planetary station (retrograde or direct)."""

    time: datetime
    station_type: str = Field(..., description="Retrograde Station or Direct Station")
    julian_day: float


class StationsResponse(BaseAstroResponse[list[StationSchema]]):
    pass
