from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class LunarPhaseSchema(BaseModel):
    """
    Metadata for a lunar phase (New, Full, or specific angle).
    """

    phase_name: str
    time: datetime
    julian_day: float
    degree: float = Field(..., description="Angular difference from Sun")


class LunarPhasesResponse(BaseAstroResponse[list[LunarPhaseSchema]]):
    pass


class EclipseSchema(BaseModel):
    """
    Solar or Lunar eclipse event.
    """

    time: datetime
    type: str
    is_solar: bool


class EclipseResponse(BaseAstroResponse[list[EclipseSchema]]):
    pass


class LunarExtremeSchema(BaseModel):
    """
    Lunar Apogee or Perigee.
    """

    time: datetime
    type: str
    julian_day: float
    distance: float = Field(..., description="Distance in Earth radii or km")


class LunarExtremeResponse(BaseAstroResponse[list[LunarExtremeSchema]]):
    pass
