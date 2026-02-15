from typing import List
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet
from ..domain.cycle import CycleEvent
from ..services.cycle_service import CycleService

class CycleEngine:
    """
    High-level orchestration for complex planetary cycles.
    """
    def __init__(self):
        self._ephemeris = Ephemeris()
        self._cycle_service = CycleService(self._ephemeris)

    def compute_synodic_cycle(self, p1: Planet, p2: Planet, start_time: Time) -> List[CycleEvent]:
        """
        Compute synodic phases between two planets.
        """
        return self._cycle_service.compute_synodic_cycle(p1, p2, start_time)

    def calculate_returns(self, planet: Planet, start_time: Time, count: int = 1) -> List[CycleEvent]:
        """
        Calculate the next N returns for a planet.
        """
        # ... logic
        return []
