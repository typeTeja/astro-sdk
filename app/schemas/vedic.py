from datetime import datetime

from pydantic import BaseModel, Field

from .astro import PlanetPositionData
from .base import BaseAstroResponse


class DashaPeriodSchema(BaseModel):
    """
    Hierarchical Vimshottari dasha period.
    """

    lord: str
    start_time: datetime
    end_time: datetime
    level: int
    sub_periods: list["DashaPeriodSchema"] | None = Field(
        None, description="Nested bhuktis/antardashas"
    )


class DashaResponse(BaseAstroResponse[list[DashaPeriodSchema]]):
    pass


class DChartData(BaseModel):
    """
    Divisional Chart positions.
    """

    division: int
    planets: list[PlanetPositionData]


class DChartResponse(BaseAstroResponse[DChartData]):
    pass


class SectorHitSchema(BaseModel):
    """
    Sectors (e.g. Gauquelin) distribution hit.
    """

    planet: str
    sector: int
    intensity: float = Field(..., description="Proximity to sector peak (0.0 to 1.0)")


class SectorResponse(BaseAstroResponse[list[SectorHitSchema]]):
    pass
