"""
Declination Parallels and Contra-Parallels

Aspects in declination (north/south celestial coordinate) rather than longitude.
Completes the aspect system with out-of-ecliptic relationships.

- Parallel: Planets at same declination (both north or both south)
- Contra-Parallel: Planets at opposite declinations (one north, one south)

Example:
    parallels = find_declination_aspects(
        planets=chart.planets,
        orb=1.0
    )
    
    for p in parallels:
        print(f"{p.p1} {p.aspect_type} {p.p2} ({p.orb}°)")
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal

from ..core.constants import Planet
from .planet import PlanetPosition


class DeclinationAspect(BaseModel):
    """
    Aspect in declination rather than longitude.
    
    Tracks parallel (same) and contra-parallel (opposite) relationships.
    """
    model_config = ConfigDict(frozen=True)
    
    p1: Planet
    p2: Planet
    p1_declination: float = Field(ge=-90.0, le=90.0, description="First planet declination")
    p2_declination: float = Field(ge=-90.0, le=90.0, description="Second planet declination")
    orb: float = Field(ge=0.0, description="Orb from exact parallel/contra-parallel")
    aspect_type: Literal["parallel", "contra_parallel"]
    
    @property
    def is_parallel(self) -> bool:
        """Check if this is a parallel (same sign declination)."""
        return self.aspect_type == "parallel"
    
    @property
    def is_contra_parallel(self) -> bool:
        """Check if this is a contra-parallel (opposite sign declination)."""
        return self.aspect_type == "contra_parallel"


def get_declination(planet_position: PlanetPosition) -> float:
    """
    Get declination for a planet position.
    
    Note: This is a placeholder. In production, declination should be
    calculated from ephemeris data or included in PlanetPosition model.
    
    Args:
        planet_position: Planet position with longitude/latitude
    
    Returns:
        Declination in degrees (-90 to +90)
        Currently returns latitude as approximation
    """
    # TODO: Calculate proper declination from ecliptic coordinates
    # For now, use latitude as rough approximation
    return planet_position.latitude


def find_declination_aspects(
    planets: List[PlanetPosition],
    orb: float = 1.0
) -> List[DeclinationAspect]:
    """
    Find parallel and contra-parallel aspects by declination.
    
    Args:
        planets: List of planet positions
        orb: Maximum orb for parallel/contra-parallel (default 1.0°)
    
    Returns:
        List of DeclinationAspect objects
    
    Examples:
        >>> # Find tight parallels
        >>> parallels = find_declination_aspects(planets, orb=0.5)
        >>> 
        >>> # Check for specific parallel
        >>> venus_jupiter = [a for a in parallels 
        >>>                  if {a.p1, a.p2} == {Planet.VENUS, Planet.JUPITER}]
    """
    aspects = []
    
    # Get declinations for all planets
    planet_decls = {}
    for p in planets:
        planet_decls[p.planet] = get_declination(p)
    
    # Check all pairs
    planet_list = list(planet_decls.keys())
    for i, p1 in enumerate(planet_list):
        for p2 in planet_list[i+1:]:
            decl1 = planet_decls[p1]
            decl2 = planet_decls[p2]
            
            # Check for parallel (same sign, similar value)
            if (decl1 >= 0 and decl2 >= 0) or (decl1 < 0 and decl2 < 0):
                orb_value = abs(abs(decl1) - abs(decl2))
                if orb_value <= orb:
                    aspects.append(DeclinationAspect(
                        p1=p1,
                        p2=p2,
                        p1_declination=decl1,
                        p2_declination=decl2,
                        orb=orb_value,
                        aspect_type="parallel"
                    ))
            
            # Check for contra-parallel (opposite signs, similar absolute values)
            else:
                orb_value = abs(abs(decl1) - abs(decl2))
                if orb_value <= orb:
                    aspects.append(DeclinationAspect(
                        p1=p1,
                        p2=p2,
                        p1_declination=decl1,
                        p2_declination=decl2,
                        orb=orb_value,
                        aspect_type="contra_parallel"
                    ))
    
    return aspects
