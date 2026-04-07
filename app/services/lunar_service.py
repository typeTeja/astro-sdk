from ..core.constants import Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..schemas.lunar import LunarExtremeSchema, LunarPhaseSchema


class LunarService:
    """
    Orchestration service for Lunar and Eclipse calculations.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris

    def get_next_phases(
        self, start_time: Time, count: int = 4, target_angle: float | None = None
    ) -> list[LunarPhaseSchema]:
        """
        Find the next N occurrences of a lunar phase.
        If target_angle is None, finds the standard 4 (NEW, 1st Qtr, FULL, 3rd Qtr).
        If target_angle is set, searches for that specific angular separation.
        """
        phases: list[LunarPhaseSchema] = []
        current_jd = start_time.julian_day

        # Determine targets
        standard_angles: list[float]
        standard_names: list[str]

        if target_angle is None:
            # 0=New, 90=1st Qtr, 180=Full, 270=3rd Qtr
            standard_angles = [0.0, 90.0, 180.0, 270.0]
            standard_names = ["NEW", "FIRST_QUARTER", "FULL", "THIRD_QUARTER"]
        else:
            standard_angles = [float(target_angle % 360)]
            standard_names = [f"PHASE_{int(target_angle)}"]

        for _ in range(count):
            # 1. Find which angle is next
            sun_pos = self.eph.calculate_planet(current_jd, Planet.SUN, sidereal=False)
            moon_pos = self.eph.calculate_planet(current_jd, Planet.MOON, sidereal=False)
            curr_diff = (moon_pos["longitude"] - sun_pos["longitude"]) % 360

            # Find next target from our list
            next_target_idx = 0
            found_target = False
            for i, angle in enumerate(standard_angles):
                if curr_diff < angle:
                    next_target_idx = i
                    found_target = True
                    break

            if not found_target:
                next_target_idx = 0

            angle_to_find = standard_angles[next_target_idx]

            # 2. Search for the exact moment
            jd_low = current_jd
            jd_high = current_jd + 30.0

            def get_angle_diff(jd: float, target: float = angle_to_find) -> float:
                s = self.eph.calculate_planet(jd, Planet.SUN, sidereal=False)
                m = self.eph.calculate_planet(jd, Planet.MOON, sidereal=False)
                diff = (m["longitude"] - s["longitude"]) % 360
                res = (diff - target + 180) % 360 - 180
                return res

            # Refine
            for _ in range(25):
                mid = (jd_low + jd_high) / 2.0
                if get_angle_diff(mid) < 0:
                    jd_low = mid
                else:
                    jd_high = mid

            found_jd = (jd_low + jd_high) / 2.0
            found_time = Time.from_julian_day(found_jd).dt

            phases.append(
                LunarPhaseSchema(
                    phase_name=standard_names[next_target_idx],
                    time=found_time,
                    julian_day=found_jd,
                    degree=angle_to_find,
                )
            )

            current_jd = found_jd + 2.0

        return phases

    def get_lunar_extremes(self, start_time: Time, count: int = 2) -> list[LunarExtremeSchema]:
        """
        Find next Apogee (max distance) and Perigee (min distance) events.
        """
        extremes: list[LunarExtremeSchema] = []
        current_jd = start_time.julian_day
        step = 0.5

        for _ in range(count):
            last_dist = self.eph.calculate_planet(current_jd, Planet.MOON)["distance"]
            current_jd += step
            curr_dist = self.eph.calculate_planet(current_jd, Planet.MOON)["distance"]

            moving_away = curr_dist > last_dist

            search_jd = current_jd
            for _ in range(60):
                search_jd += step
                d = self.eph.calculate_planet(search_jd, Planet.MOON)["distance"]
                if (moving_away and d < curr_dist) or (not moving_away and d > curr_dist):
                    jd_low = search_jd - step
                    jd_high = search_jd

                    for _ in range(15):
                        m1 = jd_low + (jd_high - jd_low) / 3
                        m2 = jd_high - (jd_high - jd_low) / 3
                        d1 = self.eph.calculate_planet(m1, Planet.MOON)["distance"]
                        d2 = self.eph.calculate_planet(m2, Planet.MOON)["distance"]

                        if moving_away:
                            if d1 < d2:
                                jd_low = m1
                            else:
                                jd_high = m2
                        else:
                            if d1 > d2:
                                jd_low = m1
                            else:
                                jd_high = m2

                    found_jd = (jd_low + jd_high) / 2.0
                    found_dist = self.eph.calculate_planet(found_jd, Planet.MOON)["distance"]
                    extremes.append(
                        LunarExtremeSchema(
                            type="APOGEE" if moving_away else "PERIGEE",
                            time=Time.from_julian_day(found_jd).dt,
                            julian_day=found_jd,
                            distance=found_dist,
                        )
                    )
                    current_jd = found_jd + 1.0
                    break
                curr_dist = d

        return extremes
