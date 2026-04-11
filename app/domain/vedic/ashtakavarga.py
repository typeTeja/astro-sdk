from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class AshtakavargaMatrix:
    values: dict[str, list[int]]
    metadata: DomainMetadata
