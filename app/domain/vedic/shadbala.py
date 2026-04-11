from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class ShadbalaScore:
    planet: str
    total_rupas: float
    metadata: DomainMetadata
