"""
Domain models for transit and progression calculations.
These are pure value objects used by the service layer;
Pydantic schema conversion happens in the API layer.
"""
from dataclasses import dataclass
from datetime import datetime

from ..core.constants import Planet


@dataclass(frozen=True)
class TransitAspect:
    """A transit planet forming an aspect to a natal position."""

    transit_planet: Planet
    natal_planet: str  # stored as name string from input schema
    aspect_type: str
    angle: float
    orb: float
    is_applying: bool


@dataclass(frozen=True)
class ProgressedChart:
    """Result of a secondary progression calculation."""

    progression_date: datetime
    # List of (planet_name, longitude, latitude, distance, speed_long, is_retrograde, sign, sign_name)
    # Stored as a list of plain dicts to avoid coupling to schema or domain planet model
    planets: list[dict[str, object]]
