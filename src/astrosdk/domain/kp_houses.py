"""
Krishnamurti Paddhati (KP) House System

KP is a sophisticated Vedic astrology system that uses:
1. Placidus houses as the base
2. Unequal house cusps
3. Sub-lord (significator) determination for precise predictions

This module implements KP-specific calculations for house divisions
used in Krishnamurti Paddhati astrology.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from ..core.constants import ZodiacSign, Planet


class KPCusp(BaseModel):
    """
    KP System house cusp with sub-lord information.
    
    In KP astrology, each cusp has:
    - Sign lord (ruler of the zodiac sign)
    - Star lord (nakshatra ruler)
    - Sub-lord (subdivision for precise timing)
    """
    model_config = ConfigDict(frozen=True)
    
    house_number: int = Field(ge=1, le=12, description="House number (1-12)")
    longitude: float = Field(ge=0.0, lt=360.0, description="Cusp longitude")
    sign_lord: Planet = Field(description="Ruler of the zodiac sign")
    star_lord: Planet = Field(description="Nakshatra (star) ruler")
    sub_lord: Planet = Field(description="Sub-division ruler for precise timing")
    
    @property
    def sign(self) -> ZodiacSign:
        """Zodiac sign of this cusp."""
        return ZodiacSign(int(self.longitude / 30))
    
    @property
    def degree_in_sign(self) -> float:
        """Degree within the zodiac sign (0-30)."""
        return self.longitude % 30.0


class KPHouseSystem(BaseModel):
    """
    Complete KP house system with all 12 cusps and sub-lords.
    
    KP houses use Placidus divisions but add:
    - Nakshatra rulership
    - Sub-lord calculation for timing
    - Specific significator rules
    """
    model_config = ConfigDict(frozen=True)
    
    cusps: List[KPCusp] = Field(min_length=12, max_length=12)
    ascendant: float = Field(ge=0.0, lt=360.0, description="Ascendant (Lagna)")
    midheaven: float = Field(ge=0.0, lt=360.0, description="Midheaven (MC)")
    
    def __getitem__(self, house_number: int) -> KPCusp:
        """Access cusp by house number (1-indexed)."""
        if not 1 <= house_number <= 12:
            raise IndexError(f"House number must be 1-12, got {house_number}")
        return self.cusps[house_number - 1]


# For KP system, we treat Ketu as the opposite node
# In Swiss Ephemeris, MEAN_NODE_OPP = -1 is Ketu
KETU = -1  # South Node (Ketu)
RAHU = Planet.MEAN_NODE  # North Node (Rahu)

# Nakshatra (Lunar Mansion) rulership
# 27 nakshatras, each 13°20' (13.333°), rulers cycle through 9 planets
NAKSHATRA_LORDS = [
    KETU,            # 1. Ashwini
    Planet.VENUS,    # 2. Bharani
    Planet.SUN,      # 3. Krittika
    Planet.MOON,     # 4. Rohini
    Planet.MARS,     # 5. Mrigashira
    RAHU,            # 6. Ardra
    Planet.JUPITER,  # 7. Punarvasu
    Planet.SATURN,   # 8. Pushya
    Planet.MERCURY,  # 9. Ashlesha
    KETU,            # 10. Magha
    Planet.VENUS,    # 11. Purva Phalguni
    Planet.SUN,      # 12. Uttara Phalguni
    Planet.MOON,     # 13. Hasta
    Planet.MARS,     # 14. Chitra
    RAHU,            # 15. Swati
    Planet.JUPITER,  # 16. Vishakha
    Planet.SATURN,   # 17. Anuradha
    Planet.MERCURY,  # 18. Jyeshtha
    KETU,            # 19. Mula
    Planet.VENUS,    # 20. Purva Ashadha
    Planet.SUN,      # 21. Uttara Ashadha
    Planet.MOON,     # 22. Shravana
    Planet.MARS,     # 23. Dhanishta
    RAHU,            # 24. Shatabhisha
    Planet.JUPITER,  # 25. Purva Bhadrapada
    Planet.SATURN,   # 26. Uttara Bhadrapada
    Planet.MERCURY,  # 27. Revati
]

# Sub-lord divisions within each nakshatra (proportional distribution)
# Each nakshatra is divided into 9 sub-parts ruled by the same cycle
SUB_LORD_SEQUENCE = [
    KETU,
    Planet.VENUS,
    Planet.SUN,
    Planet.MOON,
    Planet.MARS,
    RAHU,
    Planet.JUPITER,
    Planet.SATURN,
    Planet.MERCURY,
]

# Proportional periods (Vimshottari Dasha periods in years)
DASHA_YEARS = {
    KETU: 7,
    Planet.VENUS: 20,
    Planet.SUN: 6,
    Planet.MOON: 10,
    Planet.MARS: 7,
    RAHU: 18,
    Planet.JUPITER: 16,
    Planet.SATURN: 19,
    Planet.MERCURY: 17,
}

# Total dasha cycle = 120 years
TOTAL_DASHA_YEARS = sum(DASHA_YEARS.values())


def get_nakshatra_lord(longitude: float) -> Planet:
    """
    Get the nakshatra (star) lord for a given longitude.
    
    Args:
        longitude: Ecliptic longitude (0-360°)
    
    Returns:
        Planet ruling the nakshatra
    
    Examples:
        >>> get_nakshatra_lord(0.0)   # 0° Aries = Ashwini
        Planet.KETU
        >>> get_nakshatra_lord(30.0)  # 0° Taurus = Krittika
        Planet.SUN
    """
    # Each nakshatra is 13°20' = 13.333333°
    nakshatra_index = int(longitude / 13.333333333333334)
    return NAKSHATRA_LORDS[nakshatra_index % 27]


def get_sub_lord(longitude: float) -> Planet:
    """
    Get the sub-lord for a given longitude using Vimshottari proportions.
    
    The sub-lord is determined by dividing each nakshatra into 9 unequal parts
    proportional to the Vimshottari Dasha periods.
    
    Args:
        longitude: Ecliptic longitude (0-360°)
    
    Returns:
        Planet ruling the sub-division
    
    Examples:
        >>> get_sub_lord(0.5)  # Early Ashwini
        Planet.KETU
    """
    NAKSHATRA_SPAN = 13.333333333333334  # 13°20'
    
    # Position within current nakshatra (0 to 13.333333°)
    nak_position = longitude % NAKSHATRA_SPAN
    
    # Convert to proportional position (0 to 120)
    proportional_position = (nak_position / NAKSHATRA_SPAN) * TOTAL_DASHA_YEARS
    
    # Find which sub-lord based on cumulative periods
    cumulative = 0.0
    for planet in SUB_LORD_SEQUENCE:
        cumulative += DASHA_YEARS[planet]
        if proportional_position < cumulative:
            return planet
    
    # Fallback (should not reach here)
    return SUB_LORD_SEQUENCE[-1]


def get_sign_lord(sign: ZodiacSign) -> Planet:
    """
    Get the traditional ruler of a zodiac sign.
    
    Args:
        sign: Zodiac sign
    
    Returns:
        Planet ruling the sign
    """
    SIGN_RULERS = {
        ZodiacSign.ARIES: Planet.MARS,
        ZodiacSign.TAURUS: Planet.VENUS,
        ZodiacSign.GEMINI: Planet.MERCURY,
        ZodiacSign.CANCER: Planet.MOON,
        ZodiacSign.LEO: Planet.SUN,
        ZodiacSign.VIRGO: Planet.MERCURY,
        ZodiacSign.LIBRA: Planet.VENUS,
        ZodiacSign.SCORPIO: Planet.MARS,
        ZodiacSign.SAGITTARIUS: Planet.JUPITER,
        ZodiacSign.CAPRICORN: Planet.SATURN,
        ZodiacSign.AQUARIUS: Planet.SATURN,
        ZodiacSign.PISCES: Planet.JUPITER,
    }
    return SIGN_RULERS[sign]


def calculate_kp_houses(
    house_cusps: List[float],
    ascendant: float,
    midheaven: float
) -> KPHouseSystem:
    """
    Calculate KP house system with sub-lords from Placidus cusps.
    
    Args:
        house_cusps: List of 12 house cusp longitudes (from Placidus or similar)
        ascendant: Ascendant longitude
        midheaven: Midheaven longitude
    
    Returns:
        KPHouseSystem with all cusps and sub-lord information
    
    Examples:
        >>> # Typically called from NatalService with Placidus cusps
        >>> cusps = [0.0, 30.0, 60.0, ...]  # From Swiss Ephemeris
        >>> kp_system = calculate_kp_houses(cusps, 15.0, 285.0)
        >>> kp_system[1].sub_lord  # Get 1st house sub-lord
        Planet.VENUS
    """
    if len(house_cusps) != 12:
        raise ValueError(f"Expected 12 house cusps, got {len(house_cusps)}")
    
    kp_cusps = []
    for i, cusp_long in enumerate(house_cusps, start=1):
        sign = ZodiacSign(int(cusp_long / 30))
        
        kp_cusp = KPCusp(
            house_number=i,
            longitude=cusp_long,
            sign_lord=get_sign_lord(sign),
            star_lord=get_nakshatra_lord(cusp_long),
            sub_lord=get_sub_lord(cusp_long)
        )
        kp_cusps.append(kp_cusp)
    
    return KPHouseSystem(
        cusps=kp_cusps,
        ascendant=ascendant,
        midheaven=midheaven
    )
