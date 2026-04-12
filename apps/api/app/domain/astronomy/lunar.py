from dataclasses import dataclass
from datetime import datetime

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class LunarPhaseRecord:
    phase_name: str
    time: datetime
    metadata: DomainMetadata
