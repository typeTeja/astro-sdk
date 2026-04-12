from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time


class AstronomyCrossingService:
    """Shared 2.0 service for finding planetary crossings (returns, aspects, etc.)."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()

    def find_longitude_crossing(
        self,
        planet: Planet,
        target_longitude: float,
        start_time: Time,
        max_days: float = 400.0,
    ) -> Time:
        """
        Generic bisection-based crossing finder.
        """
        is_sidereal = self.context.zodiac.is_sidereal
        is_helio = self.context.coordinate.is_heliocentric
        
        current_jd = start_time.julian_day
        end_jd = current_jd + max_days
        
        # moon is fast, others are slower
        step = 0.5 if planet == Planet.MOON else 1.0
            
        def get_diff(jd: float) -> float:
            pos = self._ephemeris.calculate_planet(jd, planet, sidereal=is_sidereal, heliocentric=is_helio)
            return (pos["longitude"] - target_longitude + 180) % 360 - 180

        last_diff = get_diff(current_jd)
        found_window = None
        
        while current_jd < end_jd:
            next_jd = min(current_jd + step, end_jd)
            curr_diff = get_diff(next_jd)
            if last_diff * curr_diff <= 0 and abs(last_diff - curr_diff) < 180:
                found_window = (current_jd, next_jd)
                break
            last_diff = curr_diff
            current_jd = next_jd
            
        if not found_window:
            return start_time
            
        t1, t2 = found_window
        d1 = get_diff(t1)
        for _ in range(30):
            tm = (t1 + t2) / 2.0
            dm = get_diff(tm)
            if (d1 > 0) == (dm > 0):
                t1 = tm
                d1 = dm
            else:
                t2 = tm
        
        return Time.from_julian_day((t1 + t2) / 2.0)

    def find_aspect_crossings(
        self,
        p1: Planet,
        p2: Planet,
        target_angle: float,
        start_time: Time,
        end_time: Time,
    ) -> list[Time]:
        """
        Finds moments when two planets reach a specific angular separation.
        """
        is_sidereal = self.context.zodiac.is_sidereal
        is_helio = self.context.coordinate.is_heliocentric
        
        results = []
        current_jd = start_time.julian_day
        max_jd = end_time.julian_day
        step = 0.5 # half day steps for aspects
        
        def get_angle_diff(jd: float) -> float:
            pos1 = self._ephemeris.calculate_planet(jd, p1, sidereal=is_sidereal, heliocentric=is_helio)
            pos2 = self._ephemeris.calculate_planet(jd, p2, sidereal=is_sidereal, heliocentric=is_helio)
            
            # separation
            diff = abs(pos1["longitude"] - pos2["longitude"]) % 360
            if diff > 180:
                diff = 360 - diff
            
            return diff - target_angle

        last_diff = get_angle_diff(current_jd)
        
        while current_jd < max_jd:
            next_jd = min(current_jd + step, max_jd)
            curr_diff = get_angle_diff(next_jd)
            
            if last_diff * curr_diff <= 0:
                # Bisection to refine
                t1, t2 = current_jd, next_jd
                d1 = get_angle_diff(t1)
                for _ in range(25):
                    tm = (t1 + t2) / 2.0
                    dm = get_angle_diff(tm)
                    if (d1 > 0) == (dm > 0):
                        t1 = tm
                        d1 = dm
                    else:
                        t2 = tm
                results.append(Time.from_julian_day((t1 + t2) / 2.0))
            
            last_diff = curr_diff
            current_jd = next_jd
            
        return results
