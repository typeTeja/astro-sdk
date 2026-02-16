"""
Essential Dignities - Classical astrological strength classification.

Dignities describe a planet's ability to act effectively in a given sign.
This module implements traditional rulership-based dignities with configurable
rules for different astrological traditions.
"""

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Dict, Tuple, Optional
from ..core.constants import Planet, ZodiacSign

class DignityType(str, Enum):
    """Classification of planetary dignity states."""
    EXALTATION = "exaltation"          # Planet at peak strength
    OWN_SIGN = "own_sign"               # Planet in sign it rules
    MULATRIKONA = "mulatrikona"         # Special strength (Vedic)
    FRIEND = "friend"                   # Friendly placement
    NEUTRAL = "neutral"                 # Neither helped nor hindered
    ENEMY = "enemy"                     # Difficult placement
    DETRIMENT = "detriment"             # Opposite of rulership
    FALL = "fall"                       # Opposite of exaltation (weakest)

class DignityResult(BaseModel):
    """Result of dignity analysis for a planet in a sign."""
    model_config = ConfigDict(frozen=True)
    
    type: DignityType
    strength: float = Field(ge=0.0, le=100.0, description="Relative strength (0-100)")
    exact_degree: Optional[float] = Field(None, description="Exact degree of exaltation/fall if applicable")

# Traditional Western Dignity Rules
DIGNITY_RULES: Dict[Planet, Dict[str, any]] = {
    Planet.SUN: {
        "exaltation": (ZodiacSign.ARIES, 19.0),        # Exalted at 19° Aries
        "own_sign": [ZodiacSign.LEO],
        "detriment": [ZodiacSign.AQUARIUS],
        "fall": (ZodiacSign.LIBRA, 19.0)               # Fall at 19° Libra
    },
    Planet.MOON: {
        "exaltation": (ZodiacSign.TAURUS, 3.0),
        "own_sign": [ZodiacSign.CANCER],
        "detriment": [ZodiacSign.CAPRICORN],
        "fall": (ZodiacSign.SCORPIO, 3.0)
    },
    Planet.MERCURY: {
        "exaltation": (ZodiacSign.VIRGO, 15.0),
        "own_sign": [ZodiacSign.GEMINI, ZodiacSign.VIRGO],
        "detriment": [ZodiacSign.SAGITTARIUS, ZodiacSign.PISCES],
        "fall": (ZodiacSign.PISCES, 15.0)
    },
    Planet.VENUS: {
        "exaltation": (ZodiacSign.PISCES, 27.0),
        "own_sign": [ZodiacSign.TAURUS, ZodiacSign.LIBRA],
        "detriment": [ZodiacSign.SCORPIO, ZodiacSign.ARIES],
        "fall": (ZodiacSign.VIRGO, 27.0)
    },
    Planet.MARS: {
        "exaltation": (ZodiacSign.CAPRICORN, 28.0),
        "own_sign": [ZodiacSign.ARIES, ZodiacSign.SCORPIO],
        "detriment": [ZodiacSign.LIBRA, ZodiacSign.TAURUS],
        "fall": (ZodiacSign.CANCER, 28.0)
    },
    Planet.JUPITER: {
        "exaltation": (ZodiacSign.CANCER, 15.0),
        "own_sign": [ZodiacSign.SAGITTARIUS, ZodiacSign.PISCES],
        "detriment": [ZodiacSign.GEMINI, ZodiacSign.VIRGO],
        "fall": (ZodiacSign.CAPRICORN, 15.0)
    },
    Planet.SATURN: {
        "exaltation": (ZodiacSign.LIBRA, 21.0),
        "own_sign": [ZodiacSign.CAPRICORN, ZodiacSign.AQUARIUS],
        "detriment": [ZodiacSign.CANCER, ZodiacSign.LEO],
        "fall": (ZodiacSign.ARIES, 21.0)
    },
}

# Mulatrikona ranges (Vedic tradition) - (sign, start_degree, end_degree)
MULATRIKONA_RANGES: Dict[Planet, Tuple[ZodiacSign, float, float]] = {
    Planet.SUN: (ZodiacSign.LEO, 0.0, 20.0),
    Planet.MOON: (ZodiacSign.TAURUS, 4.0, 20.0),
    Planet.MERCURY: (ZodiacSign.VIRGO, 16.0, 20.0),
    Planet.VENUS: (ZodiacSign.LIBRA, 0.0, 15.0),
    Planet.MARS: (ZodiacSign.ARIES, 0.0, 12.0),
    Planet.JUPITER: (ZodiacSign.SAGITTARIUS, 0.0, 10.0),
    Planet.SATURN: (ZodiacSign.AQUARIUS, 0.0, 20.0),
}


def calculate_dignity(
    planet: Planet,
    sign: ZodiacSign,
    degree_in_sign: float,
    include_mulatrikona: bool = False
) -> DignityResult:
    """
    Calculate essential dignity for a planet in a given sign.
    
    Pure function implementing traditional dignity rules with optional
    Vedic mulatrikona ranges.
    
    Args:
        planet: Planet to analyze
        sign: Zodiac sign the planet occupies
        degree_in_sign: Degree within the sign (0-30)
        include_mulatrikona: Include Vedic mulatrikona classification
    
    Returns:
        DignityResult with classification and strength score
    
    Examples:
        >>> # Sun in Leo (own sign)
        >>> result = calculate_dignity(Planet.SUN, ZodiacSign.LEO, 10.0)
        >>> result.type
        DignityType.OWN_SIGN
        >>> result.strength
        75.0
        
        >>> # Venus exalted in Pisces
        >>> result = calculate_dignity(Planet.VENUS, ZodiacSign.PISCES, 27.0)
        >>> result.type
        DignityType.EXALTATION
        >>> result.strength
        100.0
    """
    rules = DIGNITY_RULES.get(planet, {})
    
    # Check Exaltation (highest strength)
    if "exaltation" in rules:
        exalt_sign, exalt_degree = rules["exaltation"]
        if sign == exalt_sign:
            # Strength increases as we approach exact degree
            distance_from_exact = abs(degree_in_sign - exalt_degree)
            # Full strength at exact degree, decreasing by 5% per degree
            strength = max(85.0, 100.0 - (distance_from_exact * 5.0))
            return DignityResult(
                type=DignityType.EXALTATION,
                strength=min(100.0, strength),
                exact_degree=exalt_degree
            )
    
    # Check Mulatrikona (Vedic special strength)
    if include_mulatrikona and planet in MULATRIKONA_RANGES:
        mt_sign, mt_start, mt_end = MULATRIKONA_RANGES[planet]
        if sign == mt_sign and mt_start <= degree_in_sign <= mt_end:
            return DignityResult(
                type=DignityType.MULATRIKONA,
                strength=80.0,
                exact_degree=None
            )
    
    # Check Own Sign (rulership)
    if "own_sign" in rules:
        if sign in rules["own_sign"]:
            return DignityResult(
                type=DignityType.OWN_SIGN,
                strength=75.0,
                exact_degree=None
            )
    
    # Check Fall (lowest strength)
    if "fall" in rules:
        fall_sign, fall_degree = rules["fall"]
        if sign == fall_sign:
            distance_from_exact = abs(degree_in_sign - fall_degree)
            strength = max(0.0, 15.0 - (distance_from_exact * 5.0))
            return DignityResult(
                type=DignityType.FALL,
                strength=strength,
                exact_degree=fall_degree
            )
    
    # Check Detriment
    if "detriment" in rules:
        if sign in rules["detriment"]:
            return DignityResult(
                type=DignityType.DETRIMENT,
                strength=25.0,
                exact_degree=None
            )
    
    # Neutral (no special dignity or debility)
    return DignityResult(
        type=DignityType.NEUTRAL,
        strength=50.0,
        exact_degree=None
    )


def get_dignity_score(planet: Planet, sign: ZodiacSign, degree_in_sign: float) -> float:
    """
    Get simple numeric score (0-100) for dignity strength.
    
    Convenience function for quick comparisons.
    
    Args:
        planet: Planet to analyze
        sign: Zodiac sign
        degree_in_sign: Degree within sign
    
    Returns:
        Strength score from 0 (fall) to 100 (exaltation)
    """
    result = calculate_dignity(planet, sign, degree_in_sign)
    return result.strength
