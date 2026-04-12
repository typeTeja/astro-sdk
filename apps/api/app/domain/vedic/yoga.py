from dataclasses import dataclass

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class YogaHit:
    yoga_name: str
    confidence: float
    metadata: DomainMetadata
