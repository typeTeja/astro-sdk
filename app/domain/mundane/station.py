from dataclasses import dataclass
from datetime import datetime

from ...core.constants import Planet
from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class StationEvent:
    planet: Planet
    station_type: str
    time: datetime
    metadata: DomainMetadata
