from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from app.core.constants import Planet
from app.domain.common.metadata import DomainMetadata


class EventType(StrEnum):
    INGRESS = "INGRESS"
    STATION = "STATION"
    ASPECT = "ASPECT"
    ECLIPSE = "ECLIPSE"
    DIURNAL = "DIURNAL" # Rise/Set


@dataclass(frozen=True)
class MundaneEvent:
    """Base class for all celestial events."""
    type: EventType
    time: datetime
    julian_day: float
    metadata: DomainMetadata


@dataclass(frozen=True)
class IngressEvent(MundaneEvent):
    planet: Planet
    sign_from: int
    sign_to: int
    is_retrograde: bool


@dataclass(frozen=True)
class StationEvent(MundaneEvent):
    planet: Planet
    station_type: str  # "RETROGRADE" or "DIRECT"
    speed_before: float
    speed_after: float


@dataclass(frozen=True)
class ExactAspectEvent(MundaneEvent):
    primary_planet: Planet
    secondary_planet: Planet
    aspect_type: str
    target_angle: float


@dataclass(frozen=True)
class EclipseEvent(MundaneEvent):
    eclipse_type: str  # "SOLAR" or "LUNAR"
    magnitude: float
    is_total: bool
    is_annular: bool = False
    peak_jd: float = field(default=0.0)
