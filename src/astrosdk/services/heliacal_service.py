from typing import List, Dict, Optional
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet

class HeliacalService:
    """
    Service for specialized celestial events like heliacal rising/setting
    and planetary stations.
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def calculate_heliacal_rising(
        self, 
        planet: Planet, 
        time: Time, 
        lat: float, 
        lon: float, 
        altitude: float = 0.0,
        star_name: str = ""
    ) -> Optional[Time]:
        """Calculate next heliacal rising after given time."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day, planet, lat, lon, altitude, 
            event_type=1, star_name=star_name
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None

    def calculate_heliacal_setting(
        self, 
        planet: Planet, 
        time: Time, 
        lat: float, 
        lon: float, 
        altitude: float = 0.0,
        star_name: str = ""
    ) -> Optional[Time]:
        """Calculate next heliacal setting after given time."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day, planet, lat, lon, altitude, 
            event_type=2, star_name=star_name
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None

    def find_all_stations(
        self, 
        planet: Planet, 
        year: int, 
        forward: bool = True
    ) -> List[Dict[str, any]]:
        """
        Find all stationary points (Retrograde/Direct) for a planet in a given year.
        """
        results = []
        # Start from Jan 1st of the year
        import datetime
        from datetime import timezone
        current_jd = Time(datetime.datetime(year, 1, 1, tzinfo=timezone.utc)).julian_day
        end_jd = Time(datetime.datetime(year, 12, 31, 23, 59, tzinfo=timezone.utc)).julian_day
        
        while current_jd < end_jd:
            station_jd = self.eph.calculate_stationary_point(current_jd, planet, forward=True, max_days=365)
            if station_jd is None or station_jd > end_jd:
                break
            
            # Determine type (Direct to Retrograde or Retrograde to Direct)
            # Check speed just before and after
            speed_before = self.eph.calculate_planet(station_jd - 0.01, planet)["speed_long"]
            speed_after = self.eph.calculate_planet(station_jd + 0.01, planet)["speed_long"]
            
            s_type = "Retrograde Station" if speed_before > 0 else "Direct Station"
            
            results.append({
                "time": Time.from_julian_day(station_jd),
                "type": s_type,
                "jd": station_jd
            })
            
            # Advance search window
            current_jd = station_jd + 5.0 # Skip ahead to avoid finding same point
            
        return results

    def calculate_acronychal_rising(
        self, 
        planet: Planet, 
        time: Time, 
        lat: float, 
        lon: float, 
        altitude: float = 0.0,
        star_name: str = ""
    ) -> Optional[Time]:
        """Calculate next acronychal rising (rising at sunset)."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day, planet, lat, lon, altitude, 
            event_type=5, star_name=star_name
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None

    def calculate_cosmical_setting(
        self, 
        planet: Planet, 
        time: Time, 
        lat: float, 
        lon: float, 
        altitude: float = 0.0,
        star_name: str = ""
    ) -> Optional[Time]:
        """Calculate next cosmical setting (setting at sunrise)."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day, planet, lat, lon, altitude, 
            event_type=6, star_name=star_name
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None
