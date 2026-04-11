from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class EventCluster:
    label: str
    events: tuple[str, ...]
    metadata: DomainMetadata
