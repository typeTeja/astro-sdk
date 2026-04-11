from dataclasses import dataclass
from datetime import datetime

from ...core.constants import Planet
from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class TransitWindow:
    transit_planet: Planet
    target: str
    entering: datetime
    peak: datetime
    leaving: datetime
    metadata: DomainMetadata
