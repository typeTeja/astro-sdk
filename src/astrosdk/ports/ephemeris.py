from typing import Protocol, List, Dict, Optional, Any
from astrosdk.core.time import Time
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.domain.models.planet import PlanetPosition, PlanetaryPhenomena, FixedStarPosition

class EphemerisProvider(Protocol):
    """
    Abstract interface for planetary calculations.
    """
    
    def calculate_planet(
        self, 
        time: Time, 
        planet: Planet, 
        sidereal_mode: Optional[SiderealMode] = None,
        heliocentric: bool = False,
        topocentric_coords: Optional[tuple[float, float, float]] = None # (lat, lon, alt)
    ) -> PlanetPosition:
        """Calculate position of a single planet."""
        ...

    def calculate_planets(
        self, 
        time: Time, 
        planets: List[Planet], 
        sidereal_mode: Optional[SiderealMode] = None,
        heliocentric: bool = False,
        topocentric_coords: Optional[tuple[float, float, float]] = None
    ) -> List[PlanetPosition]:
        """Batch calculate planetary positions."""
        ...
        
    def calculate_phenomena(self, time: Time, planet: Planet) -> PlanetaryPhenomena:
        """Calculate planetary phenomena (phase, magnitude, etc.)."""
        ...
        
    def calculate_fixed_star(
        self, 
        time: Time, 
        star_name: str, 
        sidereal_mode: Optional[SiderealMode] = None
    ) -> FixedStarPosition:
        """Calculate position of a fixed star."""
        ...
