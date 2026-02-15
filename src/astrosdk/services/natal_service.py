from typing import List, Dict
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet, HouseSystem, SiderealMode
from ..domain.planet import PlanetPosition
from ..domain.house import ChartHouses, HouseCusp, HouseAxes

class NatalService:
    """
    Pure service for calculating Natal Charts.
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def calculate_positions(self, time: Time, sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> List[PlanetPosition]:
        """
        Calculate all planetary positions for a given time.
        """
        # Ensure mode is set (thread-safe in Ephemeris)
        self.eph.set_sidereal_mode(sidereal_mode)
        
        jd = time.julian_day
        results = []
        
        # Calculate main planets
        for planet in Planet:
            if planet in [Planet.MEAN_NODE_OPP]: # Skip Ketu loop, calc manually
                continue
                
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
            
            # Handle Ketu (Opposite Node)
            if planet == Planet.MEAN_NODE:
                ketu_lon = (data["longitude"] + 180.0) % 360.0
                ketu = PlanetPosition(
                    planet=Planet.MEAN_NODE_OPP,
                    longitude=ketu_lon,
                    latitude=-data["latitude"], # Approx inverted
                    distance=data["distance"],
                    speed_long=data["speed_long"],
                    speed_lat=data["speed_lat"],
                    speed_dist=data["speed_dist"]
                )
                results.append(ketu)

        return results

    def calculate_houses(self, time: Time, lat: float, lon: float, 
                         system: HouseSystem = HouseSystem.PLACIDUS, 
                         sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> ChartHouses:
        """
        Calculate house cusps.
        """
        self.eph.set_sidereal_mode(sidereal_mode)
        jd = time.julian_day
        
        try:
            data = self.eph.calculate_houses(jd, lat, lon, system, sidereal=True)
        except Exception as e:
            # Fallback for high latitudes where Placidus/Koch fail
            if system in [HouseSystem.PLACIDUS, HouseSystem.KOCH]:
                # Fallback to Porphyry (System 'O') which is robust
                data = self.eph.calculate_houses(jd, lat, lon, HouseSystem.PORPHYRY, sidereal=True)
            else:
                raise
        
        cusps = []
        raw_cusps = data["cusps"]
        
        if len(raw_cusps) == 13:
            # Index 1-12 are the cusps, 0 is unused
            for i in range(1, 13):
                cusps.append(HouseCusp(number=i, longitude=raw_cusps[i]))
        else:
            # Assume 12 elements are cusps 1-12 directly
            for i in range(len(raw_cusps)):
                cusps.append(HouseCusp(number=i+1, longitude=raw_cusps[i]))
            
        axes = HouseAxes(
            ascendant=data["ascendant"],
            midheaven=data["mc"],
            descendant=(data["ascendant"] + 180) % 360,
            imum_coeli=(data["mc"] + 180) % 360,
            vertex=data["vertex"]
        )
        
        return ChartHouses(system=system, cusps=cusps, axes=axes)
