from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from app.core.constants import Planet


@dataclass(frozen=True)
class TimeWindow:
    """Represents a bounded astronomical time period."""
    planet: Planet
    start_time: datetime
    end_time: datetime
    event_type: str
    metadata: dict[str, Any] = field(default_factory=dict)
