from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .astro import PlanetPositionData
from .base import AstroTimeInput, BaseAstroResponse, GeographicLocation


from app.core.constants import HouseSystem, SiderealMode

class ChartSettings(BaseModel):
    """
    Strict configuration schema for chart generation.
    """
    house_system: HouseSystem | None = Field(default=None, description="House division system (e.g. W, P)")
    is_sidereal: bool | None = Field(default=None, description="Use sidereal zodiac (True) or tropical (False)")
    sidereal_mode: SiderealMode | None = Field(default=None, description="Ayanamsa system enum (e.g. LAHIRI)")


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


class PanchangaResponse(BaseAstroResponse[PanchangaDataSchema]):
    pass


class TransitChartData(BaseModel):
    """
    Planetary positions at a given moment.
    """

    planets: list[PlanetPositionData]


class TransitChartResponse(BaseAstroResponse[TransitChartData]):
    pass
