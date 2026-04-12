"""Schemas for the /api/v2/horizon endpoints."""
from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class RiseSetSchema(BaseModel):
    """Rise, transit, and set times for a planet."""

    planet: str
    rise: datetime | None = Field(None, description="Rise time (UTC)")
    transit: datetime | None = Field(None, description="Meridian transit time (UTC)")
    set: datetime | None = Field(None, description="Set time (UTC)")


class RiseSetResponse(BaseAstroResponse[RiseSetSchema]):
    pass


class TwilightSchema(BaseModel):
    """Civil/nautical/astronomical twilight times."""

    twilight_type: str
    dawn: datetime | None
    dusk: datetime | None


class TwilightResponse(BaseAstroResponse[TwilightSchema]):
    pass
