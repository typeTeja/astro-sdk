from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .astro import PlanetPositionData
from .base import AstroTimeInput, BaseAstroResponse, GeographicLocation


class NatalChartRequest(BaseModel):
    """
    Standard request for a 12-house natal chart.
    """

    time: AstroTimeInput
    location: GeographicLocation
    settings: dict[str, Any] | None = None


class NatalChartData(BaseModel):
    """
    Full data for a calculated natal chart.
    """

    planets: list[PlanetPositionData]
    houses: list[float] = Field(..., description="House cusps (1-12)")
    ascendant: float
    mc: float


class NatalChartResponse(BaseAstroResponse[NatalChartData]):
    pass


class PanchangaData(BaseModel):
    """
    Standard 5 elements of Vedic time calculation.
    """

    tithi: str
    nakshatra: str
    yoga: str
    karana: str
    vara: str
    sunrise: datetime
    sunset: datetime


class PanchangaResponse(BaseAstroResponse[PanchangaData]):
    pass


class TransitChartData(BaseModel):
    """
    Planetary positions at a given moment.
    """

    planets: list[PlanetPositionData]


class TransitChartResponse(BaseAstroResponse[TransitChartData]):
    pass
