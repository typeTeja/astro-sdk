from dataclasses import dataclass
from ..core.constants import Planet

@dataclass(frozen=True)
class Aspect:
    p1: Planet
    p2: Planet
    angle: float
    orb: float
    type: str  # Conjunction, Square, etc.
    applying: bool
