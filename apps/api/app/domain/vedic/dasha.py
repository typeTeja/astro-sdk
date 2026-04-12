from dataclasses import dataclass
from datetime import datetime

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class DashaPeriod:
    lord: str
    start: datetime
    end: datetime
    level: int
    metadata: DomainMetadata
