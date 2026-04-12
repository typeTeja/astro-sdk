from datetime import timedelta
from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.astronomy.lunar import LunarPhaseRecord
from app.domain.common.metadata import DomainMetadata


class AstronomyLunarService:
    """
    Native 2.0 service for lunar cycle analysis (Phases, Apogee/Perigee).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def get_next_phases(
        self, 
        start_time: Time, 
        count: int = 4
    ) -> list[LunarPhaseRecord]:
        """
        Find next N major lunar phases (New, 1st Qtr, Full, 3rd Qtr).
        Uses a high-precision binary search solver.
        """
        phases = []
        current_jd = start_time.julian_day
        
        # 0=New, 90=1st Qtr, 180=Full, 270=3rd Qtr
        target_angles = [0.0, 90.0, 180.0, 270.0]
        names = ["NEW_MOON", "FIRST_QUARTER", "FULL_MOON", "THIRD_QUARTER"]

        for _ in range(count):
            # Calculate current phase context
            s = self._eph.calculate_planet(current_jd, Planet.SUN)
            m = self._eph.calculate_planet(current_jd, Planet.MOON)
            curr_diff = (m["longitude"] - s["longitude"]) % 360
            
            # Find next target
            next_idx = 0
            for i, target in enumerate(target_angles):
                if curr_diff < target:
                    next_idx = i
                    break
            
            target_angle = target_angles[next_idx]
            
            # Refine using binary search
            low = current_jd
            high = current_jd + 31.0
            
            for _ in range(25):
                mid = (low + high) / 2.0
                ms = self._eph.calculate_planet(mid, Planet.SUN)
                mm = self._eph.calculate_planet(mid, Planet.MOON)
                diff = (mm["longitude"] - ms["longitude"]) % 360
                
                # Check crossing
                if (diff - target_angle + 180) % 360 - 180 < 0:
                    low = mid
                else:
                    high = mid
            
            found_jd = (low + high) / 2.0
            phases.append(LunarPhaseRecord(
                phase_name=names[next_idx],
                time=Time.from_julian_day(found_jd).dt,
                metadata=DomainMetadata(
                    capability="astronomy.lunar.phase",
                    maturity=self.context.feature.maturity.value,
                    fingerprint=self.context.fingerprint
                )
            ))
            current_jd = found_jd + 2.0 # Advance
            
        return phases

    def get_lunar_extremes(self, start_time: Time, count: int = 2) -> list[dict]:
        """
        Find next Apogee (max distance) and Perigee (min distance) events.
        """
        extremes = []
        current_jd = start_time.julian_day
        step = 0.5

        for _ in range(count):
            last_dist = self._eph.calculate_planet(current_jd, Planet.MOON)["distance"]
            current_jd += step
            curr_dist = self._eph.calculate_planet(current_jd, Planet.MOON)["distance"]
            moving_away = curr_dist > last_dist

            search_jd = current_jd
            for _ in range(60):
                search_jd += step
                d = self._eph.calculate_planet(search_jd, Planet.MOON)["distance"]
                if (moving_away and d < curr_dist) or (not moving_away and d > curr_dist):
                    jd_low, jd_high = search_jd - step, search_jd
                    for _ in range(15):
                        m1 = jd_low + (jd_high - jd_low) / 3
                        m2 = jd_high - (jd_high - jd_low) / 3
                        d1 = self._eph.calculate_planet(m1, Planet.MOON)["distance"]
                        d2 = self._eph.calculate_planet(m2, Planet.MOON)["distance"]
                        if moving_away:
                            if d1 < d2: jd_low = m1
                            else: jd_high = m2
                        else:
                            if d1 > d2: jd_low = m1
                            else: jd_high = m2
                    found_jd = (jd_low + jd_high) / 2.0
                    extremes.append({
                        "type": "APOGEE" if moving_away else "PERIGEE",
                        "time": Time.from_julian_day(found_jd).dt,
                        "julian_day": found_jd,
                        "distance": self._eph.calculate_planet(found_jd, Planet.MOON)["distance"],
                    })
                    current_jd = found_jd + 1.0
                    break
                curr_dist = d
        return extremes
