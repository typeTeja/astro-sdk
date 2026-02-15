from dataclasses import dataclass
from datetime import timedelta
from ..core.constants import Planet

@dataclass(frozen=True)
class CycleConfig:
    planet: Planet
    harmonic: int  # 1 = return, 2 = opposition, 4 = square
    start_long: float

@dataclass(frozen=True)
class CycleEvent:
    config: CycleConfig
    exact_time: float # Julian Day
    error_margin: float # Degrees from exact
