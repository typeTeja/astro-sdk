from dataclasses import dataclass
from datetime import date

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class MarketCycleCorrelation:
    event_name: str
    observed_date: date
    metadata: DomainMetadata
