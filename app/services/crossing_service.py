import math
import logging
from datetime import UTC
from typing import Any

from ..core.constants import Planet, SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.errors import EphemerisError
from ..core.time import Time

# Maximum iterations in find_ingresses() to prevent infinite scan loops
_MAX_INGRESS_SCAN_ITERATIONS = 50

logger = logging.getLogger(__name__)


class CrossingService:
    """
    Service for calculating planetary returns and ingresses.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris

    def find_planetary_return(
        self,
        planet: Planet,
        target_longitude: float,
        start_time: Time,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
        heliocentric: bool = False,
        max_search_years: float = 2.0,
        tolerance_seconds: float = 1.0,
    ) -> Time:
        """
        Find the exact time a planet reaches a specific longitude.
        """
        self.eph.set_sidereal_mode(sidereal_mode)

        jd_start = start_time.julian_day
        limit_days = max_search_years * 365.25

        step_days = 0.5
        if planet == Planet.MOON:
            step_days = 0.1

        jd_low = jd_start
        jd_high = jd_start + limit_days

        last_diff: float | None = None
        found_window = False

        def get_diff(jd: float) -> float:
            pos = self.eph.calculate_planet(jd, planet, sidereal=True, heliocentric=heliocentric)
            lon = pos["longitude"]
            diff = (lon - target_longitude + 180) % 360 - 180
            return diff

        curr_jd = jd_start
        while curr_jd < jd_high:
            diff = get_diff(curr_jd)
            if (
                last_diff is not None
                and abs(diff) < 90
                and abs(last_diff) < 90
                and ((last_diff < 0 and diff >= 0) or (last_diff > 0 and diff <= 0))
            ):
                jd_low = curr_jd - step_days
                jd_high = curr_jd
                found_window = True
                break
            last_diff = diff
            curr_jd += step_days

        if not found_window:
            raise EphemerisError(
                f"Could not find return for {planet.name} within {max_search_years} years."
            )

        tol_jd = tolerance_seconds / 86400.0

        while (jd_high - jd_low) > tol_jd:
            mid = (jd_low + jd_high) / 2.0
            diff = get_diff(mid)
            low_diff = get_diff(jd_low)
            if (low_diff < 0 and diff > 0) or (low_diff > 0 and diff < 0):
                jd_high = mid
            else:
                jd_low = mid

        final_jd = (jd_low + jd_high) / 2.0
        return Time.from_julian_day(final_jd)

    def find_solar_return(
        self,
        natal_sun_longitude: float,
        year: int,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
    ) -> Time:
        """Find solar return for a given year."""
        from datetime import datetime, timedelta

        start_search = Time(datetime(year, 1, 1, 0, 0, tzinfo=UTC) - timedelta(days=10))
        return self.find_planetary_return(
            Planet.SUN,
            natal_sun_longitude,
            start_search,
            sidereal_mode=sidereal_mode,
            max_search_years=1.2,
        )

    def find_lunar_return(
        self,
        natal_moon_longitude: float,
        start_time: Time,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
    ) -> Time:
        """Find next lunar return after start_time."""
        return self.find_planetary_return(
            Planet.MOON,
            natal_moon_longitude,
            start_time,
            sidereal_mode=sidereal_mode,
            max_search_years=0.1,
        )

    def find_next_ingress(
        self,
        planet: Planet,
        start_time: Time,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
        heliocentric: bool = False,
    ) -> tuple[Time, int]:
        """
        Find the next sign ingress (0, 30, 60... degree alignment).
        """
        self.eph.set_sidereal_mode(sidereal_mode)
        pos = self.eph.calculate_planet(
            start_time.julian_day, planet, sidereal=True, heliocentric=heliocentric
        )
        curr_lon = pos["longitude"]
        speed = pos["speed_long"]

        if speed >= 0:
            target_lon = (math.floor(curr_lon / 30.0) + 1) * 30.0
            if target_lon >= 360:
                target_lon = 0.0
        else:
            target_lon = math.floor(curr_lon / 30.0) * 30.0
            if target_lon < 0:
                target_lon = 330.0

        ingress_time = self.find_planetary_return(
            planet,
            target_lon,
            start_time,
            sidereal_mode=sidereal_mode,
            heliocentric=heliocentric,
            max_search_years=0.5 if planet != Planet.PLUTO else 40.0,
        )

        sign_num = int((target_lon / 30.0) % 12) + 1
        return ingress_time, sign_num

    def find_ingresses(self, planet: Planet, start_time: Time, end_time: Time) -> list[Any]:
        """
        Scan a window for all sign ingresses.
        """
        from ..domain.events import PlanetaryEvent

        results: list[Any] = []
        curr = start_time
        iterations = 0

        while curr.julian_day < end_time.julian_day and iterations < _MAX_INGRESS_SCAN_ITERATIONS:
            try:
                ing_time, sign_num = self.find_next_ingress(planet, curr)
                if ing_time.julian_day <= end_time.julian_day:
                    results.append(
                        PlanetaryEvent(
                            planet=planet,
                            event_type="INGRESS",
                            time=ing_time.dt,
                            sign_id=sign_num,
                            is_retrograde=False,
                        )
                    )
                    curr = Time.from_julian_day(ing_time.julian_day + 0.1)
                else:
                    break
            except EphemerisError:
                # Ephemeris calculation failed — log and stop the scan
                logger.exception(
                    "Ephemeris error during ingress scan for %s at JD=%.4f",
                    planet.name,
                    curr.julian_day,
                )
                break
            except Exception:
                # Unexpected error — log with traceback and abort
                logger.exception(
                    "Unexpected error during ingress scan for %s at JD=%.4f",
                    planet.name,
                    curr.julian_day,
                )
                break
            iterations += 1

        return results

    def find_stations(self, planet: Planet, start_time: Time, end_time: Time) -> list[Any]:
        """
        Scan a window for retrograde/direct stations.
        """
        from ..domain.events import PlanetaryEvent

        results: list[Any] = []
        step = 0.5
        if planet == Planet.MOON:
            return []

        jd_low = start_time.julian_day
        jd_high = end_time.julian_day

        curr_jd = jd_low
        while curr_jd < jd_high:
            jd1 = curr_jd
            jd2 = min(curr_jd + step, jd_high)

            v1 = self.eph.calculate_planet(jd1, planet)["speed_long"]
            v2 = self.eph.calculate_planet(jd2, planet)["speed_long"]

            if v1 * v2 < 0:
                j_l, j_h = jd1, jd2
                for _ in range(20):
                    mid = (j_l + j_h) / 2.0
                    vm = self.eph.calculate_planet(mid, planet)["speed_long"]
                    if (v1 > 0) == (vm > 0):
                        j_l = mid
                    else:
                        j_h = mid

                station_jd = (j_l + j_h) / 2.0
                results.append(
                    PlanetaryEvent(
                        planet=planet,
                        event_type="STATION",
                        time=Time.from_julian_day(station_jd).dt,
                        is_retrograde=(v1 > 0),
                    )
                )
            curr_jd += step

        return results

    def find_aspects(
        self, p1: Planet, p2: Planet, target_angle: float, start_time: Time, end_time: Time
    ) -> list[Any]:
        """
        Scan a window for exact aspects between two planets.
        """
        from ..domain.events import PlanetaryEvent

        results: list[Any] = []
        step = 0.5
        jd_low = start_time.julian_day
        jd_high = end_time.julian_day

        def get_diff(jd: float) -> float:
            pos1 = self.eph.calculate_planet(jd, p1, sidereal=False)
            pos2 = self.eph.calculate_planet(jd, p2, sidereal=False)
            diff = (pos1["longitude"] - pos2["longitude"]) % 360
            return (diff - target_angle + 180) % 360 - 180

        curr_jd = jd_low
        while curr_jd < jd_high:
            jd1 = curr_jd
            jd2 = min(curr_jd + step, jd_high)

            d1 = get_diff(jd1)
            d2 = get_diff(jd2)

            if d1 * d2 < 0 and abs(d1 - d2) < 180:
                jl, jh = jd1, jd2
                dl = d1
                for _ in range(20):
                    mid = (jl + jh) / 2.0
                    dm = get_diff(mid)
                    if (dl > 0) == (dm > 0):
                        jl = mid
                        dl = dm
                    else:
                        jh = mid

                aspect_jd = (jl + jh) / 2.0
                results.append(
                    PlanetaryEvent(
                        planet=p1,
                        event_type="ASPECT",
                        time=Time.from_julian_day(aspect_jd).dt,
                        sign_id=int(target_angle),
                    )
                )
            curr_jd += step
        return results
