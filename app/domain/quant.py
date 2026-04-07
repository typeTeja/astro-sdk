from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..core.constants import Planet


@dataclass(frozen=True)
class SynodicCycle:
    """
    The relative phase (0-360) between two celestial bodies.
    For example, the New Moon to New Moon cycle for Sun and Moon.
    """

    p1: Planet
    p2: Planet
    phase: float
    is_waxing: bool
    is_applying: bool  # True if the aspect is closing


@dataclass(frozen=True)
class AstroIndicator:
    """
    Quantitative metrics for a single planet at a point in time.
    """

    planet: Planet
    speed_roc: float  # Velocity Rate of Change (acceleration)
    relative_speed: float  # Current speed / Average speed
    price_mapping: float  # Longitude mapped to a price scale


@dataclass(frozen=True)
class FinancialAstroEvent:
    """
    A significant astrological event correlated with market data.
    """

    time: datetime
    event_type: str  # 'INGRESS', 'STATION', 'SYNODIC_CONJUNCTION'
    description: str
    metadata: dict[str, Any]
