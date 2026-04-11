from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class CompositeChart:
    chart_name: str
    metadata: DomainMetadata
