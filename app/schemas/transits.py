from datetime import datetime

from pydantic import BaseModel

from .astro import PlanetPositionData
from .base import BaseAstroResponse


class TransitAspectSchema(BaseModel):
    """
    Interaction between a transiting planet and a natal planet.
    """

    transit_planet: str
    natal_planet: str
    aspect_type: str
    angle: float
    orb: float
    is_applying: bool


class TransitScanData(BaseModel):
    """
    Complete set of active transits for a given time.
    """

    time: datetime
    aspects: list[TransitAspectSchema]


class TransitScanResponse(BaseAstroResponse[TransitScanData]):
    pass


class SecondaryProgressionData(BaseModel):
    """
    Progression (Day-for-a-Year) positions.
    """

    progression_date: datetime
    planets: list[PlanetPositionData]


class SecondaryProgressionResponse(BaseAstroResponse[SecondaryProgressionData]):
    pass
