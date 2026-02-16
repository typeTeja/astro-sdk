from typing import Dict, Tuple, Optional
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet, SiderealMode
from ..domain.planet import PlanetPosition

class NodeService:
    """
    Service for calculating nodes and apsides (orbital extremes).
    """
    def __init__(self, ephemeris: Ephemeris):
        self.eph = ephemeris

    def calculate_lunar_nodes(self, time: Time, true_node: bool = True) -> Tuple[PlanetPosition, PlanetPosition]:
        """
        Calculate North and South lunar nodes.
        
        Returns
        -------
        Tuple[PlanetPosition, PlanetPosition]
            (North Node, South Node)
        """
        planet = Planet.TRUE_NODE if true_node else Planet.MEAN_NODE
        jd = time.julian_day
        
        data = self.eph.calculate_planet(jd, planet, sidereal=True)
        
        north = PlanetPosition(
            planet=planet,
            longitude=data["longitude"],
            latitude=data["latitude"],
            distance=data["distance"],
            speed_long=data["speed_long"],
            speed_lat=data["speed_lat"],
            speed_dist=data["speed_dist"]
        )
        
        # South Node is strictly opposite
        south_lon = (data["longitude"] + 180.0) % 360.0
        south_planet = Planet.TRUE_NODE if true_node else Planet.MEAN_NODE # Just for reference
        
        south = PlanetPosition(
            planet=Planet.MEAN_NODE_OPP, # Reusing this for south node representation
            longitude=south_lon,
            latitude=-data["latitude"],
            distance=data["distance"],
            speed_long=data["speed_long"],
            speed_lat=data["speed_lat"],
            speed_dist=data["speed_dist"]
        )
        
        return north, south

    def calculate_lilith(self, time: Time, true_lilith: bool = False) -> PlanetPosition:
        """
        Calculate Black Moon Lilith (Lunar Apogee).
        """
        planet = Planet.LILITH_TRUE if true_lilith else Planet.LILITH_MEAN
        jd = time.julian_day
        
        data = self.eph.calculate_planet(jd, planet, sidereal=True)
        
        return PlanetPosition(
            planet=planet,
            longitude=data["longitude"],
            latitude=data["latitude"],
            distance=data["distance"],
            speed_long=data["speed_long"],
            speed_lat=data["speed_lat"],
            speed_dist=data["speed_dist"]
        )

    def calculate_planetary_nodes(self, time: Time, planet: Planet) -> Dict[str, float]:
        """
        Calculate ascending and descending nodes for a planet.
        """
        jd = time.julian_day
        data = self.eph.calculate_nodes_and_apsides(jd, planet)
        
        return {
            "ascending_node": data["ascending_node"]["longitude"],
            "descending_node": data["descending_node"]["longitude"]
        }

    def calculate_apsides(self, time: Time, planet: Planet) -> Dict[str, float]:
        """
        Calculate perihelion and aphelion for a planet.
        """
        jd = time.julian_day
        data = self.eph.calculate_nodes_and_apsides(jd, planet)
        
        return {
            "perihelion": data["perihelion"]["longitude"],
            "aphelion": data["aphelion"]["longitude"]
        }
