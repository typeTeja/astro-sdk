from dataclasses import dataclass
from datetime import datetime

from app.core.constants import Planet
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class HorizonEvent:
    planet: Planet
    event_type: str
    time: datetime
    metadata: DomainMetadata
