from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class AidenIntensityRecord:
    time: datetime
    score: float
    active_aspects_count: int
    metadata: DomainMetadata
    top_contributors: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class StellarCluster:
    center_longitude: float
    span_degrees: float
    planets: list[str]


@dataclass(frozen=True)
class ClusterIndexRecord:
    time: datetime
    stellar_density_score: float
    metadata: DomainMetadata
    clusters: list[StellarCluster] = field(default_factory=list)
