from ..core.constants import Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.quant import AstroIndicator, SynodicCycle


class AstroQuantService:
    """
    Service for calculating specialized indicators for financial astrology
    and quantitative market research.
    """

    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def calculate_synodic_phase(self, p1: Planet, p2: Planet, time: Time) -> SynodicCycle:
        """
        Calculate the phase (0-360) of the cycle between p1 and p2.
        Example: New Moon occurs when phase is 0.
        """
        jd = time.julian_day
        pos1 = self.eph.calculate_planet(jd, p1)
        pos2 = self.eph.calculate_planet(jd, p2)

        # Difference in longitude
        diff = (pos1["longitude"] - pos2["longitude"]) % 360.0

        # Waxing/Waning
        is_waxing = diff < 180.0

        # Applying/Separating check (simplified via velocity)
        v1 = pos1["speed_long"]
        v2 = pos2["speed_long"]
        rel_vel = v1 - v2

        # If relative velocity is positive, distance is increasing unless we wrap around
        # For simplicity in this quant context, we track the 'Closing' status
        is_applying = (diff > 180.0 and rel_vel > 0) or (diff < 180.0 and rel_vel < 0)

        return SynodicCycle(p1=p1, p2=p2, phase=diff, is_waxing=is_waxing, is_applying=is_applying)

    def calculate_velocity_metrics(
        self, planet: Planet, time: Time, window_days: float = 1.0
    ) -> AstroIndicator:
        """
        Calculate velocity Rate of Change (acceleration) and relative speed.
        """
        jd = time.julian_day
        p_now = self.eph.calculate_planet(jd, planet)
        p_prev = self.eph.calculate_planet(jd - window_days, planet)

        v_now = p_now["speed_long"]
        v_prev = p_prev["speed_long"]

        # Acceleration (ROC of speed)
        roc = (v_now - v_prev) / window_days

        # Average speeds (approximate for normalization)
        avg_speeds = {
            Planet.SUN: 0.9856,
            Planet.MOON: 13.176,
            Planet.MERCURY: 1.383,
            Planet.VENUS: 1.200,
            Planet.MARS: 0.524,
            Planet.JUPITER: 0.083,
            Planet.SATURN: 0.033,
            Planet.URANUS: 0.011,
            Planet.NEPTUNE: 0.006,
            Planet.PLUTO: 0.004,
        }

        rel_speed = v_now / avg_speeds.get(planet, 1.0)

        return AstroIndicator(
            planet=planet,
            speed_roc=roc,
            relative_speed=rel_speed,
            price_mapping=self.gann_price_mapping(p_now["longitude"]),
        )

    def scan_velocity_roc(
        self, planet: Planet, start_time: Time, end_time: Time, step_days: float = 1.0
    ) -> list[AstroIndicator]:
        """
        Scan a range of dates for velocity Rate of Change (ROC) and acceleration peaks.
        """
        jd_start = start_time.julian_day
        jd_end = end_time.julian_day

        results = []
        current_jd = jd_start
        while current_jd <= jd_end:
            t = Time.from_julian_day(current_jd)
            indicator = self.calculate_velocity_metrics(planet, t)
            results.append(indicator)
            current_jd += step_days

        return results

    def gann_price_mapping(self, longitude: float, scale: float = 1.0) -> float:
        """
        Map planetary longitude to a price point using W.D. Gann's
        Degrees-to-Price conversion.
        """
        return float(longitude * scale)
