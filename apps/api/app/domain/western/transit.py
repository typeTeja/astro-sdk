from dataclasses import dataclass
from datetime import datetime

from app.core.constants import Planet
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class TransitWindow:
    transit_planet: Planet
    target: str
    entering: datetime
    peak: datetime
    leaving: datetime
    metadata: DomainMetadata
@dataclass(frozen=True)
class TransitAspect:
    transit_planet: Planet
    natal_planet: str
    aspect_type: str
    angle: float
    orb: float
    is_applying: bool
    metadata: DomainMetadata
