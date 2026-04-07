from dataclasses import dataclass, field
from datetime import datetime

from ..core.constants import Planet


@dataclass
class PlanetaryEvent:
    """
    Domain model for a single celestial event (Ingress, Station, Aspect).
    Optional fields carry additional context populated by the specific service method.
    """

    planet: Planet
    event_type: str  # Use AstroEventType values: INGRESS, STATION, ASPECT, ...
    time: datetime
    sign_id: int | None = None
    is_retrograde: bool = False
    # Ingress-specific fields
    from_sign: str | None = None
    to_sign: str | None = None
    # Station-specific fields
    station_type: str | None = None  # "RETROGRADE" or "DIRECT"
    # Aspect-specific fields
    target_angle: float | None = None
