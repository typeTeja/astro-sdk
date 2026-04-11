from dataclasses import dataclass

from ...core.constants import Planet
from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class PlanetSnapshot:
    planet: Planet
    longitude: float
    latitude: float
    distance: float
    metadata: DomainMetadata
