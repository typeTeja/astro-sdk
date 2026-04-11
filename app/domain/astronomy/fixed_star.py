from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class FixedStarContact:
    star_name: str
    longitude: float
    latitude: float
    metadata: DomainMetadata
