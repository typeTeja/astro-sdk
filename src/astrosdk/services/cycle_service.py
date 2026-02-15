from typing import List
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet
from ..domain.cycle import CycleEvent, CycleConfig

class CycleService:
    """
    Service for calculating planetary returns and synodic cycles.
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def compute_return(self, planet: Planet, target_long: float, start_time: Time, window_days: float = 400.0) -> CycleEvent:
        """
        Computes the next time a planet reaches a target longitude.
        Uses a fixed search window and bisection refinement.
        """
        jd_start = start_time.julian_day
        # Rough step for discovery (Solar return vs Moon return)
        # We search from start_time forward.
        
        step = 0.5 # 12 hours check
        current_jd = jd_start
        end_jd = jd_start + window_days # Default search window
        
        pos = self.eph.calculate_planet(current_jd, planet, sidereal=True)
        last_diff = (pos["longitude"] - target_long + 180) % 360 - 180
        
        while current_jd < end_jd:
            next_jd = current_jd + step
            pos = self.eph.calculate_planet(next_jd, planet, sidereal=True)
            current_diff = (pos["longitude"] - target_long + 180) % 360 - 180
            
            if (last_diff < 0 and current_diff >= 0) or (last_diff > 0 and current_diff <= 0):
                # Crossing found
                exact_jd = self._refine_return(planet, target_long, current_jd, next_jd)
                return CycleEvent(
                    config=CycleConfig(planet=planet, harmonic=1, start_long=target_long),
                    exact_time=exact_jd,
                    error_margin=abs(current_diff) # This will be refined
                )
            
            last_diff = current_diff
            current_jd = next_jd
            
        raise Exception(f"Return not found for {planet} within {window_days} days")

    def _refine_return(self, planet: Planet, target_lon: float, jd1: float, jd2: float, tolerance: float = 1e-7) -> float:
        low = jd1
        high = jd2
        for _ in range(30):
            mid = (low + high) / 2
            pos = self.eph.calculate_planet(mid, planet, sidereal=True)
            diff = (pos["longitude"] - target_lon + 180) % 360 - 180
            
            if diff > 0:
                high = mid
            else:
                low = mid
            if abs(high - low) < tolerance:
                break
        return (low + high) / 2

    def compute_synodic_cycle(self, p1: Planet, p2: Planet, start_time: Time) -> List[CycleEvent]:
        """
        Computes the synodic cycle phases between two planets.
        """
        # ...
        return []
