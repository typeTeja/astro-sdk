from dataclasses import dataclass
from datetime import datetime

from ..astronomy.planet import PlanetSnapshot
from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class WesternChart:
    time: datetime
    planets: tuple[PlanetSnapshot, ...]
    metadata: DomainMetadata
