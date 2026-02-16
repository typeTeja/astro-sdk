import swisseph as swe
from typing import Dict, Optional, Tuple
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet

class HorizonService:
    """
    Service for calculating rise, set, and transit times (Horizon events).
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def calculate_event(
        self, 
        planet: Planet, 
        date: Time, 
        lat: float, 
        lon: float, 
        altitude: float = 0.0, 
        is_rise: bool = True,
        rsmi_extra: int = 0
    ) -> Optional[Time]:
        """
        Calculate rise or set time for a planet at a specific location and date.
        """
        jd = date.julian_day
        res_jd = self.eph.calculate_rise_set(jd, planet, lat, lon, altitude, is_rise=is_rise, rsmi_extra=rsmi_extra)
        return Time.from_julian_day(res_jd) if res_jd else None

    def calculate_sunrise(self, date: Time, lat: float, lon: float, altitude: float = 0.0) -> Optional[Time]:
        """Calculate sunrise."""
        return self.calculate_event(Planet.SUN, date, lat, lon, altitude, is_rise=True)

    def calculate_sunset(self, date: Time, lat: float, lon: float, altitude: float = 0.0) -> Optional[Time]:
        """Calculate sunset."""
        return self.calculate_event(Planet.SUN, date, lat, lon, altitude, is_rise=False)

    def calculate_transit(self, planet: Planet, date: Time, lat: float, lon: float, altitude: float = 0.0) -> Optional[Time]:
        """Calculate meridian transit (culmination) time."""
        jd = date.julian_day
        res_jd = self.eph.calculate_transit(jd, planet, lat, lon, altitude)
        return Time.from_julian_day(res_jd) if res_jd else None

    def calculate_twilight(
        self, 
        date: Time, 
        lat: float, 
        lon: float, 
        altitude: float = 0.0,
        twilight_type: str = "civil"
    ) -> Dict[str, Optional[Time]]:
        """
        Calculate dawn and dusk times for different twilight types.
        twilight_type: 'civil' (-6°), 'nautical' (-12°), 'astronomical' (-18°)
        """
        types = {
            "civil": swe.BIT_CIVIL_TWILIGHT,
            "nautical": swe.BIT_NAUTIC_TWILIGHT,
            "astronomical": swe.BIT_ASTRO_TWILIGHT
        }
        
        if twilight_type not in types:
            raise ValueError(f"Unknown twilight type: {twilight_type}. Must be one of {list(types.keys())}")
            
        bit = types[twilight_type]
        
        # Dawn (rise) and Dusk (set)
        dawn = self.calculate_event(Planet.SUN, date, lat, lon, altitude, is_rise=True, rsmi_extra=bit)
        dusk = self.calculate_event(Planet.SUN, date, lat, lon, altitude, is_rise=False, rsmi_extra=bit)
        
        return {
            "dawn": dawn,
            "dusk": dusk
        }
