from dataclasses import dataclass
from datetime import datetime

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class ProgressedChart:
    progression_type: str
    progression_date: datetime
    metadata: DomainMetadata
