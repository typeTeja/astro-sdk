from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from app.core.constants import Planet
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class CycleCorrelation:
    planet: Planet
    event_type: str
    start_time: datetime
    end_time: datetime
    metadata: DomainMetadata
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MarketCycleCorrelation:
    event_name: str
    observed_date: date
    metadata: DomainMetadata
