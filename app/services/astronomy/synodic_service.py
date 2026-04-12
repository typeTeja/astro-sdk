from typing import Any

from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata


class AstronomySynodicService:
    """
    Native 2.0 service for planetary synodic events (Conjunctions/Oppositions).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def find_next_event(
        self,
        p1: Planet,
        p2: Planet,
        start_time: Time,
        target_angle: float = 0.0,
        max_days: float = 2000.0
    ) -> dict[str, Any]:
        """
        Find exact time of next crossing of target angular separation.
        """
        current_jd = start_time.julian_day
        step = 2.0

        def get_diff(jd: float) -> float:
            pos1 = self._eph.calculate_planet(jd, p1, sidereal=False)
            pos2 = self._eph.calculate_planet(jd, p2, sidereal=False)
            diff = (pos1["longitude"] - pos2["longitude"]) % 360
            return (diff - target_angle + 180) % 360 - 180

        # Scan for crossing window
        jd_low = current_jd
        found = False
        for i in range(int(max_days / step)):
            j1 = current_jd + (i * step)
            j2 = j1 + step
            d1, d2 = get_diff(j1), get_diff(j2)
            if d1 * d2 < 0 and abs(d1 - d2) < 180:
                jd_low = j1
                found = True
                break

        if not found:
            return {}

        # Refine using bisection
        jd_high = jd_low + step
        d_low = get_diff(jd_low)
        for _ in range(25):
            mid = (jd_low + jd_high) / 2.0
            d_mid = get_diff(mid)
            if (d_low > 0) == (d_mid > 0):
                jd_low = mid
                d_low = d_mid
            else:
                jd_high = mid

        final_jd = (jd_low + jd_high) / 2.0
        return {
            "p1": p1.name,
            "p2": p2.name,
            "target_angle": target_angle,
            "time": Time.from_julian_day(final_jd).dt,
            "metadata": DomainMetadata(
                capability="astronomy.synodic",
                maturity=self.context.feature.maturity.value,
                fingerprint=self.context.fingerprint
            )
        }

    def calculate_phase(self, p1: Planet, p2: Planet, time: Time) -> dict[str, Any]:
        """
        Calculate relative phase (0-360) and applying/separating status.
        """
        pos1 = self._eph.calculate_planet(time.julian_day, p1, sidereal=False)
        pos2 = self._eph.calculate_planet(time.julian_day, p2, sidereal=False)

        diff = (pos1["longitude"] - pos2["longitude"]) % 360

        # Determine if applying (speed check)
        v1 = pos1["speed_long"]
        v2 = pos2["speed_long"]
        rel_v = v1 - v2

        # Heuristic: if relative velocity points toward conjunction/opposition
        # This is a simplification but fulfills the current research contract.
        is_applying = (rel_v > 0 and diff > 180) or (rel_v < 0 and diff < 180)

        return {
            "p1": p1.name,
            "p2": p2.name,
            "angle": diff,
            "is_applying": is_applying,
            "metadata": DomainMetadata(
                capability="astronomy.synodic.phase",
                maturity=self.context.feature.maturity.value,
                fingerprint=self.context.fingerprint
            )
        }
