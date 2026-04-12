from dataclasses import dataclass

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class VargaChart:
    division: str
    metadata: DomainMetadata
