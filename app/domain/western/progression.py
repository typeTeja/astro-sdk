from dataclasses import dataclass
from datetime import datetime
from app.domain.common.metadata import DomainMetadata
from app.domain.astronomy.planet import PlanetSnapshot


@dataclass(frozen=True)
class ProgressedChart:
    """AstroSDK 2.0 progressed state."""
    natal_time: datetime
    progressed_time: datetime
    target_time: datetime
    planets: tuple[PlanetSnapshot, ...]
    metadata: DomainMetadata
