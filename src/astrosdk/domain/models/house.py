from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import List
from astrosdk.core.constants import HouseSystem, ZodiacSign

class HouseCusp(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    number: int
    longitude: float

    @computed_field
    @property
    def sign(self) -> ZodiacSign:
        return ZodiacSign(int(self.longitude / 30))

class HouseAxes(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    ascendant: float
    midheaven: float
    descendant: float
    imum_coeli: float
    vertex: float

class ChartHouses(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    system: HouseSystem
    cusps: List[HouseCusp]
    axes: HouseAxes
