from typing import List, Optional
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet, MAX_SEARCH_DAYS, SiderealMode
from ..core.errors import SearchRangeTooLargeError
from ..domain.event import AstroEvent, EclipseEvent
from .aspect_service import AspectService
from ..domain.planet import PlanetPosition

class EventService:
    """
    Service for scanning and detecting astrological events.
    """
    def __init__(self, ephemeris: Ephemeris, aspect_service: Optional[AspectService] = None):
        self.eph = ephemeris
        self.aspect_service = aspect_service or AspectService()

    def scan_ingresses(self, planet: Planet, start_time: Time, end_time: Time, 
                       step_days: float = 1.0, 
                       sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> List[AstroEvent]:
        """
        Scan for sign ingresses within a time range.
        Uses a step-discovery followed by bisection refinement.
        """
        self.eph.set_sidereal_mode(sidereal_mode)
        events = []
        current_jd = start_time.julian_day
        end_jd = end_time.julian_day
        
        if (end_jd - current_jd) > MAX_SEARCH_DAYS:
            raise SearchRangeTooLargeError(f"Search range exceeds maximum allowed limit of {MAX_SEARCH_DAYS} days.")

        # Get initial sign
        pos = self.eph.calculate_planet(current_jd, planet, sidereal=True)
        last_sign = int(pos["longitude"] / 30)
        
        while current_jd < end_jd:
            next_jd = min(current_jd + step_days, end_jd)
            pos = self.eph.calculate_planet(next_jd, planet, sidereal=True)
            current_sign = int(pos["longitude"] / 30)
            
            if current_sign != last_sign:
                # Ingress found between current_jd and next_jd
                exact_jd = self._refine_ingress(planet, current_jd, next_jd, last_sign, current_sign)
                events.append(AstroEvent(
                    type="INGRESS",
                    primary_body=planet,
                    secondary_body=Planet.SUN, # Placeholder for "Space"
                    julian_day=exact_jd,
                    data={"sign_from": str(last_sign), "sign_to": str(current_sign)}
                ))
            
            last_sign = current_sign
            current_jd = next_jd
            
        return events

    def scan_stations(self, planet: Planet, start_time: Time, end_time: Time, 
                      step_days: float = 1.0,
                      sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> List[AstroEvent]:
        """
        Scan for retrograde/direct stations (speed crossing zero).
        """
        self.eph.set_sidereal_mode(sidereal_mode)
        events = []
        current_jd = start_time.julian_day
        end_jd = end_time.julian_day
        
        if (end_jd - current_jd) > MAX_SEARCH_DAYS:
            raise SearchRangeTooLargeError(f"Search range exceeds maximum allowed limit of {MAX_SEARCH_DAYS} days.")

        pos = self.eph.calculate_planet(current_jd, planet, sidereal=True)
        last_speed = pos["speed_long"]
        
        while current_jd < end_jd:
            next_jd = min(current_jd + step_days, end_jd)
            pos = self.eph.calculate_planet(next_jd, planet, sidereal=True)
            current_speed = pos["speed_long"]
            
            if (last_speed > 0 and current_speed < 0) or (last_speed < 0 and current_speed > 0):
                # Station found
                exact_jd = self._refine_station(planet, current_jd, next_jd)
                events.append(AstroEvent(
                    type="STATION",
                    primary_body=planet,
                    secondary_body=Planet.SUN,
                    julian_day=exact_jd,
                    data={"speed_before": f"{last_speed:.6f}", "speed_after": f"{current_speed:.6f}"}
                ))
                
            last_speed = current_speed
            current_jd = next_jd
            
        return events

    def _refine_ingress(self, planet: Planet, jd1: float, jd2: float, s1: int, s2: int, tolerance: float = 1e-7) -> float:
        """Bisection for ingress refinement."""
        target_lon = s2 * 30.0
        # Handle Pisces -> Aries wrap
        if s1 == 11 and s2 == 0:
            target_lon = 0.0
            
        low = jd1
        high = jd2
        for _ in range(30): # Fixed iterations for deterministic precision
            mid = (low + high) / 2
            pos = self.eph.calculate_planet(mid, planet, sidereal=True)
            lon = pos["longitude"]
            
            # Normalize longitude relative to target for wrap-around cases
            diff = (lon - target_lon + 180) % 360 - 180
            
            if diff > 0:
                high = mid
            else:
                low = mid
            if abs(high - low) < tolerance:
                break
        return (low + high) / 2

    def _refine_station(self, planet: Planet, jd1: float, jd2: float, tolerance: float = 1e-7) -> float:
        """Bisection for station refinement (speed = 0)."""
        low = jd1
        high = jd2
        pos1 = self.eph.calculate_planet(jd1, planet, sidereal=True)
        v1 = pos1["speed_long"]
        
        for _ in range(30):
            mid = (low + high) / 2
            pos = self.eph.calculate_planet(mid, planet, sidereal=True)
            v_mid = pos["speed_long"]
            
            if (v1 > 0 and v_mid > 0) or (v1 < 0 and v_mid < 0):
                low = mid
                v1 = v_mid
            else:
                high = mid
            if abs(high - low) < tolerance:
                break
        return (low + high) / 2

    def scan_aspects(self, p1: Planet, p2: Planet, start_time: Time, end_time: Time) -> List[AstroEvent]:
        """
        Scan for exact aspects between two planets.
        """
        events = []
        # Implementation logic for aspect precision scanning
        # ...
        return events
    def find_next_solar_eclipse(self, start_time: Time) -> EclipseEvent:
        """
        Finds the next solar eclipse globally.
        """
        res = self.eph.search_solar_eclipse(start_time.julian_day)
        return EclipseEvent(
            type="SOLAR",
            julian_day=res["peak_jd"], # We use peak_jd as the primary JD
            is_total=res["magnitude"] >= 1.0,
            is_annular=False, # Need more Swiss data for precise flag
            magnitude=res["magnitude"],
            peak_jd=res["peak_jd"]
        )

    def find_next_lunar_eclipse(self, start_time: Time) -> EclipseEvent:
        """
        Finds the next lunar eclipse.
        """
        res = self.eph.search_lunar_eclipse(start_time.julian_day)
        return EclipseEvent(
            type="LUNAR",
            julian_day=res["peak_jd"],
            is_total=res["magnitude"] >= 1.0,
            is_annular=False,
            magnitude=res["magnitude"],
            peak_jd=res["peak_jd"]
        )

    def get_rise_set(self, planet: Planet, time: Time, lat: float, lon: float, alt: float = 0.0):
        """
        Calculate rise and set times for a planet at a specific location.
        """
        # We need to wrap swe.rise_trans properly in Ephemeris or call it here
        # For rise_trans, we need to set_topo first
        import swisseph as swe
        self.eph.set_topocentric(lat, lon, alt)
        
        # flags: 0 for rise, 1 for set
        # This is a bit complex for a single call, usually rise_trans returns 
        # the next event. 
        # Let's use a simplified wrapper if possible or direct call for now.
        
        # tret is the result Julian Day
        # flags for rise: swe.CALC_RISE
        res_rise = swe.rise_trans(time.julian_day, planet, swe.FLG_SWIEPH, swe.CALC_RISE, lon, lat, alt, 0, 0)
        res_set = swe.rise_trans(time.julian_day, planet, swe.FLG_SWIEPH, swe.CALC_SET, lon, lat, alt, 0, 0)
        
        return {
            "rise": res_rise[0] if res_rise else None,
            "set": res_set[0] if res_set else None
        }
