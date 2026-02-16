"""
Harmonic Charts Module

Generate harmonic divisional charts (H2-H12) by multiplying planetary positions.
Used for uncovering hidden patterns and relationships in natal charts.

Harmonic 2 (H2): Emphasizes partnerships and polarities
Harmonic 3 (H3): Creativity and expression
Harmonic 4 (H4): Structure and foundation
Harmonic 5 (H5): Creativity and manifestation
Harmonic 7 (H7): Spiritual and inspirational
Harmonic 9 (H9): Completion and fulfillment

Example:
    # Generate 5th harmonic chart
    h5_positions = calculate_harmonic_positions(natal_positions, harmonic=5)
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List
from ..core.constants import Planet, ZodiacSign


class HarmonicPosition(BaseModel):
    """
    Planet position in a harmonic chart.
    
    Calculated by multiplying the natal longitude by the harmonic number.
    """
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    natal_longitude: float = Field(ge=0.0, lt=360.0)
    harmonic: int = Field(ge=1, le=360, description="Harmonic number (2-12 most common)")
    harmonic_longitude: float = Field(ge=0.0, lt=360.0)
    
    @property
    def sign(self) -> ZodiacSign:
        """Zodiac sign in harmonic chart."""
        return ZodiacSign(int(self.harmonic_longitude / 30))
    
    @property
    def sign_degree(self) -> float:
        """Degree within sign in harmonic chart."""
        return self.harmonic_longitude % 30.0


class HarmonicChart(BaseModel):
    """
    Complete harmonic chart with all planet positions.
    
    Contains the harmonic positions of all planets for a specific harmonic.
    """
    model_config = ConfigDict(frozen=True)
    
    harmonic: int = Field(ge=1, le=360)
    positions: List[HarmonicPosition]
    
    def get_planet(self, planet: Planet) -> HarmonicPosition | None:
        """Get specific planet from harmonic chart."""
        for pos in self.positions:
            if pos.planet == planet:
                return pos
        return None


def calculate_harmonic_longitude(natal_longitude: float, harmonic: int) -> float:
    """
    Calculate harmonic longitude from natal position.
    
    Args:
        natal_longitude: Natal longitude (0-360)
        harmonic: Harmonic number (typically 2-12)
    
    Returns:
        Harmonic longitude (0-360)
    
    Examples:
        >>> calculate_harmonic_longitude(100.0, 2)  # H2
        200.0
        >>> calculate_harmonic_longitude(100.0, 5)  # H5
        140.0
        >>> calculate_harmonic_longitude(300.0, 3)  # H3  
        180.0
    """
    return (natal_longitude * harmonic) % 360.0


def calculate_harmonic_positions(
    natal_positions: List,
    harmonic: int
) -> HarmonicChart:
    """
    Generate harmonic chart from natal positions.
    
    Args:
        natal_positions: List of PlanetPosition objects from natal chart
        harmonic: Harmonic number (2-12 most common)
    
    Returns:
        HarmonicChart with all harmonic positions
    
    Example:
        >>> from astrosdk import calculate_natal_chart
        >>> natal = calculate_natal_chart(...)
        >>> 
        >>> # Generate 5th harmonic
        >>> h5 = calculate_harmonic_positions(natal.planets, 5)
        >>> 
        >>> # Check Sun in H5
        >>> sun_h5 = h5.get_planet(Planet.SUN)
        >>> print(f"Sun H5: {sun_h5.harmonic_longitude:.2f}°")
    """
    harmonic_positions = []
    
    for natal_pos in natal_positions:
        h_long = calculate_harmonic_longitude(natal_pos.longitude, harmonic)
        
        h_pos = HarmonicPosition(
            planet=natal_pos.planet,
            natal_longitude=natal_pos.longitude,
            harmonic=harmonic,
            harmonic_longitude=h_long
        )
        harmonic_positions.append(h_pos)
    
    return HarmonicChart(
        harmonic=harmonic,
        positions=harmonic_positions
    )


def find_harmonic_aspects(
    harmonic_chart: HarmonicChart,
    orb: float = 1.0
) -> List[tuple[Planet, Planet, float]]:
    """
    Find close conjunctions in harmonic chart.
    
    In harmonic charts, conjunctions are the primary aspect to examine.
    
    Args:
        harmonic_chart: Harmonic chart to analyze
        orb: Maximum orb for conjunction (default 1.0°)
    
    Returns:
        List of (planet1, planet2, separation) tuples
    
    Example:
        >>> h5 = calculate_harmonic_positions(positions, 5)
        >>> aspects = find_harmonic_aspects(h5, orb=2.0)
        >>> for p1, p2, orb in aspects:
        >>>     print(f"{p1.name}-{p2.name}: {orb:.2f}°")
    """
    aspects = []
    positions = harmonic_chart.positions
    
    for i, pos1 in enumerate(positions):
        for pos2 in positions[i+1:]:
            # Calculate angular separation
            diff = abs(pos1.harmonic_longitude - pos2.harmonic_longitude)
            if diff > 180:
                diff = 360 - diff
            
            if diff <= orb:
                aspects.append((pos1.planet, pos2.planet, diff))
    
    return aspects
