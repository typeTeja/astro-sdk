from dataclasses import dataclass
from datetime import datetime

from ..core.constants import Planet


@dataclass(frozen=True)
class TimeWindow:
    """A bounded structural time event window (e.g. shadow period mapping)."""

    planet: Planet
    start_time: datetime
    end_time: datetime
    event_type: str
    metadata: dict[str, str | float]


@dataclass(frozen=True)
class MarketCycleCorrelation:
    """
    Representation of an astronomical cycle structure.
    Strictly provides boundaries for statistical study.
    """

    cycle_name: str
    start_time: datetime
    peak_time: datetime | None
    end_time: datetime | None
    planets_involved: list[Planet]
    degree_bounds: tuple[float, float] | None = None
