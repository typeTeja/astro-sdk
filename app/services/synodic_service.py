from ..core.constants import Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time


class SynodicService:
    """
    Search engine for planetary synodic events (Conjunctions/Oppositions).
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris

    def find_next_event(
        self,
        p1: Planet,
        p2: Planet,
        start_time: Time,
        target_angle: float = 0.0,  # 0=Conjunction, 180=Opposition
        max_days: float = 1000.0,
    ) -> tuple[Time, float] | None:
        """
        Find the exact time of the next synodic event between two planets.
        """
        current_jd = start_time.julian_day
        step = 2.0

        def get_diff(jd: float) -> float:
            pos1 = self.eph.calculate_planet(jd, p1, sidereal=False)
            pos2 = self.eph.calculate_planet(jd, p2, sidereal=False)
            diff = (pos1["longitude"] - pos2["longitude"]) % 360
            res = (diff - target_angle + 180) % 360 - 180
            return res

        jd_low = current_jd
        found_window = False

        for i in range(int(max_days / step)):
            jd1 = current_jd + i * step
            jd2 = jd1 + step

            d1 = get_diff(jd1)
            d2 = get_diff(jd2)

            if d1 * d2 < 0 and abs(d1 - d2) < 180:
                jd_low = jd1
                found_window = True
                break

        if not found_window:
            return None

        # 2. Refine window (Bisection)
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
        return Time.from_julian_day(final_jd), target_angle
