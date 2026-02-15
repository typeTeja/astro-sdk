from dataclasses import dataclass
from typing import List
from ..core.constants import HouseSystem, ZodiacSign

@dataclass(frozen=True)
class HouseCusp:
    number: int
    longitude: float

    @property
    def sign(self) -> ZodiacSign:
        return ZodiacSign(int(self.longitude / 30))

@dataclass(frozen=True)
class HouseAxes:
    ascendant: float
    midheaven: float
    descendant: float
    imum_coeli: float
    vertex: float

@dataclass(frozen=True)
class ChartHouses:
    system: HouseSystem
    cusps: List[HouseCusp]
    axes: HouseAxes
