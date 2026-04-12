from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .astro import PlanetPositionData
from .base import AstroTimeInput, BaseAstroResponse, GeographicLocation


from app.core.constants import HouseSystem, SiderealMode

from .settings import ChartSettings


class NatalChartRequest(BaseModel):
    """
    Standard request for a 12-house natal chart.
    """

    time: AstroTimeInput
    location: GeographicLocation
    settings: ChartSettings | None = Field(default=None)


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


class PanchangaDataSchema(BaseModel):
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


class PanchangaRequest(BaseModel):
    """
    Request parameters for Vedic Panchanga calculation.
    """
    time: AstroTimeInput
    location: GeographicLocation
    settings: ChartSettings | None = Field(default=None)


class PanchangaResponse(BaseAstroResponse[PanchangaDataSchema]):
    pass


class TransitRequest(BaseModel):
    """
    Request parameters for current planetary transit calculation.
    """
    time: AstroTimeInput
    location: GeographicLocation | None = None
    settings: ChartSettings | None = Field(default=None)


class TransitChartData(BaseModel):
    """
    Planetary positions at a given moment.
    """

    planets: list[PlanetPositionData]


class TransitChartResponse(BaseAstroResponse[TransitChartData]):
    pass
