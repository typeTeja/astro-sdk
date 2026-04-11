from dataclasses import dataclass

from ...core.constants import Planet
from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class SynastryAspect:
    primary_planet: Planet
    secondary_planet: Planet
    aspect_type: str
    orb: float
    metadata: DomainMetadata
