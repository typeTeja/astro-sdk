from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class VargaChart:
    division: str
    metadata: DomainMetadata
