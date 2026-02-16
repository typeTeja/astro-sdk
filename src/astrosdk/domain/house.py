from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import List
from ..core.constants import HouseSystem, ZodiacSign

class HouseCusp(BaseModel):
    """Individual house cusp position."""
    model_config = ConfigDict(frozen=True)
    
    number: int = Field(ge=1, le=12, description="House number (1-12)")
    longitude: float = Field(ge=0.0, lt=360.0, description="Ecliptic longitude of cusp")

    @computed_field
    @property
    def sign(self) -> ZodiacSign:
        """Zodiac sign of this cusp."""
        return ZodiacSign(int(self.longitude / 30))

class HouseAxes(BaseModel):
    """Major house axis points."""
    model_config = ConfigDict(frozen=True)
    
    ascendant: float = Field(ge=0.0, lt=360.0, description="Ascendant (1st house cusp)")
    midheaven: float = Field(ge=0.0, lt=360.0, description="Midheaven (MC, 10th house cusp)")
    descendant: float = Field(ge=0.0, lt=360.0, description="Descendant (7th house cusp)")
    imum_coeli: float = Field(ge=0.0, lt=360.0, description="Imum Coeli (IC, 4th house cusp)")
    vertex: float = Field(ge=0.0, lt=360.0, description="Vertex (ecliptic-prime vertical intersection)")

class ChartHouses(BaseModel):
    """Complete house system calculation."""
    model_config = ConfigDict(frozen=True)
    
    system: HouseSystem
    cusps: List[HouseCusp] = Field(min_length=12, max_length=12, description="12 house cusps")
    axes: HouseAxes
