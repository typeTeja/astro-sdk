from dataclasses import dataclass

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class ResearchSeries:
    series_name: str
    rows: tuple[dict[str, str], ...]
    metadata: DomainMetadata
