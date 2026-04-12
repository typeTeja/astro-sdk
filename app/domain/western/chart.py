from dataclasses import dataclass
from datetime import datetime

from app.domain.astronomy.house import ChartHouses
from app.domain.astronomy.planet import PlanetSnapshot
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class WesternChart:
    time: datetime
    planets: tuple[PlanetSnapshot, ...]
    metadata: DomainMetadata
    houses: ChartHouses | None = None
