from dataclasses import dataclass

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class AshtakavargaMatrix:
    matrix: list[int]
    metadata: DomainMetadata
