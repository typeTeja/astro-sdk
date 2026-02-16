from typing import Tuple, Optional, List
import math
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet, SiderealMode
from ..core.errors import EphemerisError

class CrossingService:
    """
    Service for calculating planetary returns and ingresses.
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def find_planetary_return(
        self,
        planet: Planet,
        target_longitude: float,
        start_time: Time,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
        heliocentric: bool = False,
        max_search_years: float = 2.0,
        tolerance_seconds: float = 1.0
    ) -> Time:
        """
        Find the exact time a planet reaches a specific longitude.
        Used for Solar Returns, Lunar Returns, and other planetary returns.
        
        Parameters
        ----------
        planet : Planet
            The planet to track
        target_longitude : float
            Final destination longitude (0-360)
        start_time : Time
            When to start searching
        sidereal_mode : SiderealMode
            Ayanamsa to use
        heliocentric : bool
            Whether to use heliocentric coordinates
        max_search_years : float
            Maximum distance to look ahead
        tolerance_seconds : float
            Precision required for the time (default: 1 second)
            
        Returns
        -------
        Time
            The exact time of the return
        """
        self.eph.set_sidereal_mode(sidereal_mode)
        
        # Binary search for the moment
        # Initial bounds: start_time to start_time + max_search_years
        jd_start = start_time.julian_day
        # Estimate daily motion to find a narrow window first
        # Sun: ~1 deg/day, Moon: ~13 deg/day
        
        # For now, let's use a robust iterative refinement
        t_current = jd_start
        # Search range in days
        limit_days = max_search_years * 365.25
        
        # 1. Broad search: Find the window where the planet crosses the target
        # We step through time and check for crossing
        step_days = 0.5 # Default broad step
        if planet == Planet.MOON:
            step_days = 0.1 # Moon is faster
            
        jd_low = jd_start
        jd_high = jd_start + limit_days
        
        last_diff = None
        found_window = False
        
        # We need to handle the 360/0 wraparound
        def get_diff(jd):
            pos = self.eph.calculate_planet(jd, planet, sidereal=True, heliocentric=heliocentric)
            lon = pos["longitude"]
            diff = (lon - target_longitude + 180) % 360 - 180
            return diff

        # Search for crossing
        curr_jd = jd_start
        while curr_jd < jd_high:
            diff = get_diff(curr_jd)
            if last_diff is not None:
                # We only care about crossings where the current diff is near zero
                # and transitioned through it. Modulo wrap at 180/-180 also flips sign,
                # so we check that we are in the "front half" of the circle relative to target.
                if abs(diff) < 90 and abs(last_diff) < 90:
                    if (last_diff < 0 and diff >= 0) or (last_diff > 0 and diff <= 0):
                        # Crossing found between curr_jd - step_days and curr_jd
                        jd_low = curr_jd - step_days
                        jd_high = curr_jd
                        found_window = True
                        break
            last_diff = diff
            curr_jd += step_days
            
        if not found_window:
            raise EphemerisError(f"Could not find return for {planet.name} within {max_search_years} years.")
            
        # 2. Refine window (Binary search)
        # tolerance in JD units (1 second = 1 / 86400 days)
        tol_jd = tolerance_seconds / 86400.0
        
        while (jd_high - jd_low) > tol_jd:
            mid = (jd_low + jd_high) / 2.0
            diff = get_diff(mid)
            
            # Since we found a crossing, we know the signs of last_diff was different
            # We need to know if it's direct or retrograde to know which way to go
            # But get_diff already tells us the "signed distance"
            
            # Let's check start diff
            low_diff = get_diff(jd_low)
            if (low_diff < 0 and diff > 0) or (low_diff > 0 and diff < 0):
                jd_high = mid
            else:
                jd_low = mid
                
        final_jd = (jd_low + jd_high) / 2.0
        return Time.from_julian_day(final_jd)

    def find_solar_return(self, natal_sun_longitude: float, year: int, sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> Time:
        """Find solar return for a given year."""
        from datetime import datetime, timezone, timedelta
        # Search starting slightly before the year starts to catch early returns (e.g. Dec 31)
        start_search = Time(datetime(year, 1, 1, 0, 0, tzinfo=timezone.utc) - timedelta(days=10))
        return self.find_planetary_return(Planet.SUN, natal_sun_longitude, start_search, sidereal_mode=sidereal_mode, max_search_years=1.2)

    def find_lunar_return(self, natal_moon_longitude: float, start_time: Time, sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> Time:
        """Find next lunar return after start_time."""
        return self.find_planetary_return(Planet.MOON, natal_moon_longitude, start_time, sidereal_mode=sidereal_mode, max_search_years=0.1)

    def find_next_ingress(
        self,
        planet: Planet,
        start_time: Time,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
        heliocentric: bool = False
    ) -> Tuple[Time, int]:
        """
        Find the next sign ingress (0, 30, 60... degree alignment).
        
        Returns
        -------
        Tuple[Time, int]
            (Time of ingress, Sign number 1-12)
        """
        # 1. Current position
        self.eph.set_sidereal_mode(sidereal_mode)
        pos = self.eph.calculate_planet(start_time.julian_day, planet, sidereal=True, heliocentric=heliocentric)
        curr_lon = pos["longitude"]
        
        # 2. Find target ingress longitude
        # If moving direct, target is next 30 deg boundary
        # If moving retrograde, target is previous 30 deg boundary
        speed = pos["speed_long"]
        
        if speed >= 0:
            target_lon = (math.floor(curr_lon / 30.0) + 1) * 30.0
            if target_lon >= 360: target_lon = 0
        else:
            target_lon = math.floor(curr_lon / 30.0) * 30.0
            if target_lon < 0: target_lon = 330
            
        # 3. Use find_planetary_return to get exact time
        ingress_time = self.find_planetary_return(
            planet, 
            target_lon, 
            start_time, 
            sidereal_mode=sidereal_mode, 
            heliocentric=heliocentric,
            max_search_years=0.5 if planet != Planet.PLUTO else 40.0 # Pluto is slow
        )
        
        # 4. Determine which sign it entered
        # Sign number: 1=Aries, 2=Taurus...
        sign_num = int((target_lon / 30.0) % 12) + 1
        
        return ingress_time, sign_num
