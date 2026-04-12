from dataclasses import dataclass
from datetime import datetime

from app.domain.astronomy.planet import PlanetSnapshot
from app.domain.common.metadata import DomainMetadata
from app.domain.research.correlation import MarketCycleCorrelation
from app.domain.research.dataset import DatasetExport
from app.domain.research.series import ResearchSeries


@dataclass(frozen=True)
class WesternChart:
    time: datetime
    planets: tuple[PlanetSnapshot, ...]
    metadata: DomainMetadata
