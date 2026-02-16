"""
Combustion detection for planetary positions.

Combustion occurs when a planet is too close to the Sun, traditionally
believed to weaken the planet's influence. This module provides precise
orb-based detection with configurable thresholds.
"""

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from ..core.constants import Planet

class CombustionState(str, Enum):
    """State of planetary combustion relative to the Sun."""
    COMBUST = "combust"           # Within combustion orb (very close)
    UNDER_BEAMS = "under_beams"   # Within 17° but outside combustion orb
    CAZIMI = "cazimi"             # Exact conjunction (within 17 arcminutes)
    FREE = "free"                 # Outside all solar influence orbs

class CombustionResult(BaseModel):
    """Result of combustion analysis for a planet."""
    model_config = ConfigDict(frozen=True)
    
    state: CombustionState
    orb_from_sun: float = Field(ge=0.0, description="Angular distance from Sun in degrees")
    threshold_used: float = Field(gt=0.0, description="Combustion threshold applied")
    is_cazimi: bool = Field(description="True if within 17 arcminutes (heart of the Sun)")

# Default combustion orbs (in degrees) from traditional astrology
DEFAULT_COMBUSTION_ORBS = {
    Planet.MOON: 12.0,
    Planet.MERCURY: 14.0,  # Mercury can be "cazimi" when very close
    Planet.VENUS: 8.0,
    Planet.MARS: 17.0,
    Planet.JUPITER: 11.0,
    Planet.SATURN: 15.0,
    Planet.URANUS: 10.0,
    Planet.NEPTUNE: 10.0,
    Planet.PLUTO: 10.0,
}

# Cazimi threshold (17 arcminutes = 0.283°)
CAZIMI_ORB = 0.283


def calculate_combustion(
    planet_longitude: float,
    sun_longitude: float,
    planet: Planet,
    custom_threshold: float = None
) -> CombustionResult:
    """
    Calculate combustion state for a planet relative to the Sun.
    
    Pure function with no side effects. Uses traditional orbs by default,
    but allows custom thresholds for research purposes.
    
    Args:
        planet_longitude: Ecliptic longitude of the planet (0-360°)
        sun_longitude: Ecliptic longitude of the Sun (0-360°)
        planet: Planet enum to determine default orb
        custom_threshold: Optional custom combustion orb (overrides default)
    
    Returns:
        CombustionResult with state, orb distance, and cazimi flag
    
    Examples:
        >>> # Mercury 5° from Sun
        >>> result = calculate_combustion(120.0, 115.0, Planet.MERCURY)
        >>> result.state
        CombustionState.COMBUST
        
        >>> # Jupiter 20° from Sun (free)
        >>> result = calculate_combustion(120.0, 100.0, Planet.JUPITER)
        >>> result.state
        CombustionState.FREE
    """
    # Calculate shortest arc between planet and Sun
    diff = abs(planet_longitude - sun_longitude)
    if diff > 180:
        diff = 360 - diff
    
    orb_from_sun = diff
    
    # Determine threshold
    if custom_threshold is not None:
        threshold = custom_threshold
    else:
        threshold = DEFAULT_COMBUSTION_ORBS.get(planet, 10.0)
    
    # Check cazimi (heart of the Sun) first - most powerful state
    if orb_from_sun <= CAZIMI_ORB:
        return CombustionResult(
            state=CombustionState.CAZIMI,
            orb_from_sun=orb_from_sun,
            threshold_used=threshold,
            is_cazimi=True
        )
    
    # Check combustion
    if orb_from_sun <= threshold:
        return CombustionResult(
            state=CombustionState.COMBUST,
            orb_from_sun=orb_from_sun,
            threshold_used=threshold,
            is_cazimi=False
        )
    
    # Check under the beams (17° traditional threshold)
    if orb_from_sun <= 17.0:
        return CombustionResult(
            state=CombustionState.UNDER_BEAMS,
            orb_from_sun=orb_from_sun,
            threshold_used=threshold,
            is_cazimi=False
        )
    
    # Free from solar influence
    return CombustionResult(
        state=CombustionState.FREE,
        orb_from_sun=orb_from_sun,
        threshold_used=threshold,
        is_cazimi=False
    )


def is_combust(planet_longitude: float, sun_longitude: float, planet: Planet) -> bool:
    """
    Simple boolean check for combustion.
    
    Convenience function for quick checks without full analysis.
    
    Args:
        planet_longitude: Planet's ecliptic longitude
        sun_longitude: Sun's ecliptic longitude
        planet: Planet type
    
    Returns:
        True if planet is combust (excluding cazimi)
    """
    result = calculate_combustion(planet_longitude, sun_longitude, planet)
    return result.state == CombustionState.COMBUST
