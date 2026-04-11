from ...contexts import CalculationContext
from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.ephemeris_context import EphemerisContext
from ...core.time import Time
from ...domain.planet import PlanetPosition
from ...domain.common.metadata import DomainMetadata


class AstronomyNodeService:
    """
    Native 2.0 service for calculating nodes and apsides (orbital extremes).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def get_lunar_nodes(
        self, 
        time: Time, 
        true_node: bool = True
    ) -> tuple[PlanetPosition, PlanetPosition]:
        """
        Calculate North and South lunar nodes.
        """
        planet = Planet.TRUE_NODE if true_node else Planet.MEAN_NODE
        is_sidereal = self.context.zodiac.zodiac == "sidereal" or self.context.zodiac.sidereal_mode is not None
        sid_mode = self.context.zodiac.sidereal_mode or SiderealMode.LAHIRI

        with EphemerisContext(sid_mode=sid_mode):
            data = self._eph.calculate_planet(time.julian_day, planet, sidereal=is_sidereal)
            
            north = PlanetPosition(
                planet=planet,
                longitude=data["longitude"],
                latitude=data["latitude"],
                distance=data["distance"],
                speed_long=data["speed_long"]
            )
            
            # South node is exactly opposite
            south_lon = (data["longitude"] + 180.0) % 360.0
            south = PlanetPosition(
                planet=Planet.MEAN_NODE_OPP, # Representation
                longitude=south_lon,
                latitude=-data["latitude"],
                distance=data["distance"],
                speed_long=data["speed_long"]
            )
            
            return north, south

    def get_lilith(self, time: Time, true_lilith: bool = False) -> PlanetPosition:
        """
        Calculate Black Moon Lilith (Lunar Apogee).
        """
        planet = Planet.LILITH_TRUE if true_lilith else Planet.LILITH_MEAN
        is_sidereal = self.context.zodiac.zodiac == "sidereal" or self.context.zodiac.sidereal_mode is not None
        sid_mode = self.context.zodiac.sidereal_mode or SiderealMode.LAHIRI

        with EphemerisContext(sid_mode=sid_mode):
            data = self._eph.calculate_planet(time.julian_day, planet, sidereal=is_sidereal)
            return PlanetPosition(
                planet=planet,
                longitude=data["longitude"],
                latitude=data["latitude"],
                distance=data["distance"],
                speed_long=data["speed_long"],
            )

    def get_planetary_nodes(self, time: Time, planet: Planet) -> dict[str, float]:
        """
        Calculate ascending and descending nodes for a planet.
        """
        data = self._eph.calculate_nodes_and_apsides(time.julian_day, planet)
        return {
            "ascending_node": data["ascending_node"]["longitude"],
            "descending_node": data["descending_node"]["longitude"],
        }

    def get_apsides(
        self, 
        time: Time, 
        planet: Planet
    ) -> dict[str, float]:
        """
        Calculate perihelion and aphelion for a planet using 2.0 pattern.
        """
        data = self._eph.calculate_nodes_and_apsides(time.julian_day, planet)
        
        return {
            "perihelion": data["perihelion"]["longitude"],
            "aphelion": data["aphelion"]["longitude"],
            "metadata": DomainMetadata(
                capability="astronomy.apsides",
                maturity=self.context.feature.maturity.value,
                fingerprint=self.context.fingerprint
            )
        }
