from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
 AidenIntensityRecord: # Using a fresh name to avoid confusion
    time: datetime
    score: float
    active_aspects_count: int
    top_contributors: list[dict[str, Any]] = field(default_factory=list)
    metadata: DomainMetadata = field(default_factory=DomainMetadata)


@dataclass(frozen=True)
class StellarCluster:
    center_longitude: float
    span_degrees: float
    planets: list[str]


@dataclass(frozen=True)
class ClusterIndexRecord:
    time: datetime
    stellar_density_score: float
    clusters: list[StellarCluster] = field(default_factory=list)
    metadata: DomainMetadata = field(default_factory=DomainMetadata)
