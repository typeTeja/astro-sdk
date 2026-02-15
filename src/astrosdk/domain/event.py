from dataclasses import dataclass
from typing import Dict
from ..core.constants import Planet

@dataclass(frozen=True)
class AstroEvent:
    type: str  # Ingress, Station, Aspect
    primary_body: Planet
    secondary_body: Planet
    julian_day: float
    data: Dict[str, str] # Metadata
@dataclass(frozen=True)
class EclipseEvent:
    type: str  # Solar, Lunar
    julian_day: float
    is_total: bool
    is_annular: bool
    magnitude: float
    peak_jd: float
    # Add other eclipse-specific metadata as needed
