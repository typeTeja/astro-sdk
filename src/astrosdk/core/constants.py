from enum import Enum, IntEnum

class ZodiacSign(IntEnum):
    ARIES = 0
    TAURUS = 1
    GEMINI = 2
    CANCER = 3
    LEO = 4
    VIRGO = 5
    LIBRA = 6
    SCORPIO = 7
    SAGITTARIUS = 8
    CAPRICORN = 9
    AQUARIUS = 10
    PISCES = 11

class HouseSystem(str, Enum):
    PLACIDUS = 'P'
    KOCH = 'K'
    PORPHYRY = 'O'
    REGIOMONTANUS = 'R'
    CAMPANUS = 'C'
    EQUAL = 'E'
    WHOLE_SIGN = 'W'
    VEDIC = 'V' # Equal house from Ascendant (approx)

class Planet(IntEnum):
    # Swiss Ephemeris IDs
    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9
    MEAN_NODE = 10  # Rahu (Mean)
    TRUE_NODE = 11  # Rahu (True)
    MEAN_NODE_OPP = -1 # Ketu (Mean)
    
    # Asteroids (Main Belt)
    CHIRON = 15
    CERES = 17
    PALLAS = 18
    JUNO = 19
    VESTA = 20
    
class SiderealMode(IntEnum):
    LAHIRI = 1
    RAMAN = 3
    KRISHNAMURTI = 5
    FAGAN_BRADLEY = 0

# --- Enterprise Hardening Policies ---

# Ephemeris Engines
EPHE_SWISSEPH = 2 # swe.FLG_SWIEPH
EPHE_JPLEPH = 1   # swe.FLG_JPLEPH

# Defaults
DEFAULT_EPHE_FLAG = EPHE_SWISSEPH
DEFAULT_TIDAL = 999999 # swe.TIDAL_AUTOMATIC
DEFAULT_SIDEREAL = SiderealMode.LAHIRI

# Security Policy: Only allow historically/astronomically verified bodies by default
ALLOWED_PLANETS = {
    Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS, Planet.MARS,
    Planet.JUPITER, Planet.SATURN, Planet.URANUS, Planet.NEPTUNE, Planet.PLUTO,
    Planet.TRUE_NODE, Planet.MEAN_NODE,
    Planet.CHIRON, Planet.CERES, Planet.PALLAS, Planet.JUNO, Planet.VESTA
}

# Performance Guardrails
MAX_SEARCH_DAYS = 36525 # ~100 years
