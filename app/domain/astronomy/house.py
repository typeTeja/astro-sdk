from dataclasses import dataclass

from app.core.constants import HouseSystem, ZodiacSign
from app.domain.common.metadata import DomainMetadata


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
    cusps: list[HouseCusp]
    axes: HouseAxes
    metadata: DomainMetadata
