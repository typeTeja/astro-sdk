from dataclasses import dataclass
from datetime import datetime

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class ReturnChart:
    return_type: str
    exact_time: datetime
    metadata: DomainMetadata
