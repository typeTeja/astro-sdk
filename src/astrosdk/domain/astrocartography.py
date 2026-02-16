"""
Astro-Cartography Module

Calculate planetary lines and parans for location-based astrology.
Maps where planets are on angles (Ascendant, MC, Descendant, IC) globally.

Example:
    # Find where Jupiter is on MC
    jupiter_mc_line = calculate_planetary_line(
        planet_longitude=150.0,
        planet_declination=20.0,
        line_type="MC"
    )
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, List, Optional
from math import degrees, radians, sin, cos, asin, atan2
from ..core.constants import Planet


class PlanetaryLine(BaseModel):
    """
    Geographic line where a planet is on a specific angle.
    
    AS: Planet rising (on Ascendant)
    MC: Planet culminating (on Midheaven)
    DS: Planet setting (on Descendant)
    IC: Planet anti-culminating (on IC)
    """
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    line_type: Literal["AS", "MC", "DS", "IC"]
    planet_longitude: float = Field(ge=0.0, lt=360.0)
    planet_declination: float = Field(ge=-90.0, le=90.0)
    
    def get_latitude_at_longitude(self, longitude: float) -> Optional[float]:
        """
        Calculate latitude where this line crosses a given longitude.
        
        Args:
            longitude: Geographic longitude (-180 to 180)
        
        Returns:
            Geographic latitude (-90 to 90) or None if line doesn't cross
        
        Note:
            This is a simplified implementation. Full astro-cartography
            requires precise angular calculations.
        """
        # Simplified calculation - in production would use proper
        # spherical trigonometry
        if self.line_type in ["AS", "DS"]:
            # Rising/Setting lines depend on declination
            return self.planet_declination
        elif self.line_type == "MC":
            # MC line is where planet longitude matches RAMC
            return 0.0  # Simplified - would cross equator
        else:  # IC
            return 0.0
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.planet.name} {self.line_type} Line"


class Paran(BaseModel):
    """
    Paran: Two planets simultaneously on angles at a location.
    
    Example: Jupiter on AS while Saturn on MC at specific location.
    """
    model_config = ConfigDict(frozen=True)
    
    planet1: Planet
    angle1: Literal["AS", "MC", "DS", "IC"]
    planet2: Planet
    angle2: Literal["AS", "MC", "DS", "IC"]
    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.planet1.name} {self.angle1} / {self.planet2.name} {self.angle2}"


class AstroMap(BaseModel):
    """
    Complete astro-cartography map with all planetary lines.
    
    Shows where each planet is angular around the world.
    """
    model_config = ConfigDict(frozen=True)
    
    lines: List[PlanetaryLine]
    parans: List[Paran] = Field(default_factory=list)
    
    def get_lines_for_planet(self, planet: Planet) -> List[PlanetaryLine]:
        """Get all lines for a specific planet."""
        return [line for line in self.lines if line.planet == planet]
    
    def get_lines_by_type(self, line_type: Literal["AS", "MC", "DS", "IC"]) -> List[PlanetaryLine]:
        """Get all lines of a specific type."""
        return [line for line in self.lines if line.line_type == line_type]


def calculate_planetary_line(
    planet: Planet,
    planet_longitude: float,
    planet_declination: float,
    line_type: Literal["AS", "MC", "DS", "IC"]
) -> PlanetaryLine:
    """
    Calculate a single planetary line.
    
    Args:
        planet: Planet
        planet_longitude: Planet's ecliptic longitude
        planet_declination: Planet's declination
        line_type: Type of line (AS/MC/DS/IC)
    
    Returns:
        PlanetaryLine object
    
    Example:
        >>> # Jupiter MC line
        >>> jup_mc = calculate_planetary_line(
        >>>     Planet.JUPITER, 150.0, 20.0, "MC"
        >>> )
    """
    return PlanetaryLine(
        planet=planet,
        line_type=line_type,
        planet_longitude=planet_longitude,
        planet_declination=planet_declination
    )


def calculate_astromap(
    planet_positions: List,
    declinations: Optional[List[float]] = None
) -> AstroMap:
    """
    Calculate complete astro-cartography map.
    
    Generates all 4 lines (AS, MC, DS, IC) for each planet.
    
    Args:
        planet_positions: List of PlanetPosition objects
        declinations: Optional list of declinations (uses latitude if None)
    
    Returns:
        AstroMap with all planetary lines
    
    Example:
        >>> from astrosdk import calculate_natal_chart
        >>> chart = calculate_natal_chart(...)
        >>> 
        >>> # Generate astro-cartography map
        >>> astro_map = calculate_astromap(chart.planets)
        >>> 
        >>> # Find where Sun is on MC
        >>> sun_mc_lines = [line for line in astro_map.lines
        >>>                 if line.planet == Planet.SUN and line.line_type == "MC"]
    """
    lines = []
    
    for i, pos in enumerate(planet_positions):
        # Use declination if provided, otherwise use latitude as approximation
        decl = declinations[i] if declinations and i < len(declinations) else pos.latitude
        
        # Generate all 4 lines for each planet
        for line_type in ["AS", "MC", "DS", "IC"]:
            line = PlanetaryLine(
                planet=pos.planet,
                line_type=line_type,
                planet_longitude=pos.longitude,
                planet_declination=decl
            )
            lines.append(line)
    
    return AstroMap(lines=lines)


def find_location_planets_on_angles(
    astro_map: AstroMap,
    latitude: float,
    longitude: float,
    orb_degrees: float = 1.0
) -> List[tuple[Planet, str]]:
    """
    Find which planets are on angles at a specific location.
    
    Args:
        astro_map: AstroMap to search
        latitude: Geographic latitude (-90 to 90)
        longitude: Geographic longitude (-180 to 180)
        orb_degrees: Allowable orb in degrees
    
    Returns:
        List of (planet, angle) tuples for planets on angles
    
    Example:
        >>> astro_map = calculate_astromap(positions)
        >>> 
        >>> # Check New York City (40.7°N, 74.0°W)
        >>> on_angles = find_location_planets_on_angles(
        >>>     astro_map, 40.7, -74.0, orb_degrees=2.0
        >>> )
        >>> for planet, angle in on_angles:
        >>>     print(f"{planet.name} on {angle}")
    """
    # Simplified implementation
    # In production, would calculate exact angles for location
    # and check which planets are within orb
    
    results = []
    
    # This is a placeholder that shows the structure
    # Real implementation requires complex spherical calculations
    for line in astro_map.lines:
        # Would check if line passes near this lat/long
        pass
    
    return results
