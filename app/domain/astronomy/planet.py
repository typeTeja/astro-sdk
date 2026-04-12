from dataclasses import dataclass

from app.core.constants import Planet
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class PlanetSnapshot:
    planet: Planet
    longitude: float
    latitude: float
    distance: float
    metadata: DomainMetadata
