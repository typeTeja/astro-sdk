from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class EclipseRecord:
    eclipse_type: str
    peak_jd: float
    magnitude: float
    metadata: DomainMetadata
