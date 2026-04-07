from dataclasses import dataclass
from datetime import datetime

from ..core.constants import Planet


@dataclass(frozen=True)
class AstroIntensity:
    """Score reflecting concurrent exact aspects (0-100 scale)."""

    time: datetime
    score: float
    active_aspects_count: int
    top_contributors: list[dict[str, str | float]]


@dataclass(frozen=True)
class ClusterIndex:
    """Stellium tracking: multiple planets in narrow degree bands."""

    time: datetime
    stellar_density_score: float
    clusters: list[dict[str, str | list[Planet] | float]]
