from typing import List, Dict, Tuple
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet

class ParanService:
    """
    Service for calculating Parans (simultaneous horizon/meridian events).
    A Paran occurs when two bodies hit any of the four angles at the same time.
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def find_parans(
        self, 
        time: Time, 
        lat: float, 
        lon: float, 
        altitude: float = 0.0,
        orb_minutes: float = 5.0
    ) -> List[Dict[str, any]]:
        """
        Find all parans occurring on the calendar day of the given time.
        """
        # 1. Get all rise/set/transit times for all planets for this day
        # Start from midnight
        import datetime
        from datetime import timezone
        midnight = Time(datetime.datetime(time.dt.year, time.dt.month, time.dt.day, tzinfo=timezone.utc))
        jd = midnight.julian_day
        
        events = []
        planets_to_check = [p for p in Planet if p <= Planet.PLUTO or p == Planet.MOON]
        
        for p in planets_to_check:
            # Rise
            r = self.eph.calculate_rise_set(jd, p, lat, lon, altitude, is_rise=True)
            if r: events.append({"planet": p, "type": "Rise", "jd": r})
            
            # Set
            s = self.eph.calculate_rise_set(jd, p, lat, lon, altitude, is_rise=False)
            if s: events.append({"planet": p, "type": "Set", "jd": s})
            
            # Transit (Upper)
            t = self.eph.calculate_transit(jd, p, lat, lon, altitude)
            if t: events.append({"planet": p, "type": "Transit", "jd": t})
            
            # IC (Lower Transit) - use rsmi_extra for lower transit
            # swe.CALC_ITRANSIT is for lower transit
            # I need to check the value of CALC_ITRANSIT
            import swisseph as swe
            ic = self.eph.calculate_rise_set(jd, p, lat, lon, altitude, rsmi_extra=swe.CALC_ITRANSIT)
            if ic: events.append({"planet": p, "type": "IC", "jd": ic})

        # 2. Compare all pairs
        results = []
        orb_jd = orb_minutes / (24 * 60)
        
        for i in range(len(events)):
            for j in range(i + 1, len(events)):
                e1 = events[i]
                e2 = events[j]
                
                if abs(e1["jd"] - e2["jd"]) <= orb_jd:
                    results.append({
                        "p1": e1["planet"],
                        "type1": e1["type"],
                        "p2": e2["planet"],
                        "type2": e2["type"],
                        "time": Time.from_julian_day((e1["jd"] + e2["jd"]) / 2.0),
                        "orb_minutes": abs(e1["jd"] - e2["jd"]) * 24 * 60
                    })
                    
        return results
