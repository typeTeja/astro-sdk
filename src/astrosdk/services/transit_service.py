from typing import List
from datetime import timedelta
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet, SiderealMode
from ..domain.planet import PlanetPosition

class TransitService:
    """
    Service for calculating planetary transits over time.
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def get_daily_positions(self, start_time: Time, days: int, planet: Planet, sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> List[PlanetPosition]:
        """
        Calculate position of a single planet once per day for N days.
        """
        self.eph.set_sidereal_mode(sidereal_mode)
        results = []
        
        start_dt = start_time.dt
        
        for i in range(days):
            current_dt = start_dt + timedelta(days=i)
            t = Time(current_dt)
            jd = t.julian_day
            
            data = self.eph.calculate_planet(jd, planet, sidereal=True)
             
            p = PlanetPosition(
                planet=planet,
                longitude=data["longitude"],
                latitude=data["latitude"],
                distance=data["distance"],
                speed_long=data["speed_long"],
                speed_lat=data["speed_lat"],
                speed_dist=data["speed_dist"]
            )
            results.append(p)
            
        return results
