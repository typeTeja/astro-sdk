from dataclasses import dataclass
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class FixedStarPosition:
    """AstroSDK 2.0 fixed star spatial snapshot."""
    name: str
    longitude: float
    latitude: float
    magnitude: float
    metadata: DomainMetadata
