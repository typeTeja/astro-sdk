from dataclasses import dataclass
from datetime import datetime

from ..core.constants import Planet


@dataclass
class PlanetaryEvent:
    """
    Core domain model for a celestial event (Ingress, Station).
    """

    planet: Planet
    event_type: str  # INGRESS, STATION
    time: datetime
    sign_id: int | None = None
    is_retrograde: bool = False
