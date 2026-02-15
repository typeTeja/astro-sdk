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
    """
    All ayanamsa systems supported by Swiss Ephemeris.
    Values correspond to Swiss Ephemeris sidereal mode constants.
    """
    # Main Traditional Systems
    FAGAN_BRADLEY = 0          # Fagan/Bradley (Western sidereal)
    LAHIRI = 1                 # Lahiri (Indian government standard)
    DELUCE = 2                 # De Luce
    RAMAN = 3                  # B.V. Raman
    USHASHASHI = 4             # Usha/Shashi
    KRISHNAMURTI = 5           # Krishnamurti (KP)
    DJWHAL_KHUL = 6           # Djwhal Khul
    YUKTESHWAR = 7            # Sri Yukteshwar
    JN_BHASIN = 8             # J.N. Bhasin
    BABYLONIAN_KUGLER1 = 9    # Babylonian (Kugler 1)
    BABYLONIAN_KUGLER2 = 10   # Babylonian (Kugler 2)
    BABYLONIAN_KUGLER3 = 11   # Babylonian (Kugler 3)
    BABYLONIAN_HUBER = 12     # Babylonian (Huber)
    BABYLONIAN_ETPSC = 13     # Babylonian (ETPSC)
    ALDEBARAN_15TAU = 14      # Aldebaran at 15 Taurus
    HIPPARCHOS = 15           # Hipparchos
    SASSANIAN = 16            # Sassanian
    GALCENT_0SAG = 17         # Galactic Center at 0 Sagittarius
    J2000 = 18                # J2000
    J1900 = 19                # J1900
    B1950 = 20                # B1950
    
    # Vedic/Hindu Systems
    SURYASIDDHANTA = 21       # Suryasiddhanta
    SURYASIDDHANTA_MSUN = 22  # Suryasiddhanta (mean Sun)
    ARYABHATA = 23            # Aryabhata
    ARYABHATA_MSUN = 24       # Aryabhata (mean Sun)
    SS_REVATI = 25            # Suryasiddhanta (Revati)
    SS_CITRA = 26             # Suryasiddhanta (Citra)
    TRUE_CITRA = 27           # True Citra
    TRUE_REVATI = 28          # True Revati
    TRUE_PUSHYA = 29          # True Pushya (Panchang Puspakara)
    
    # Galactic Systems
    GALCENT_RGILBRAND = 30    # Galactic Center (Gil Brand)
    GALEQU_IAU1958 = 31       # Galactic Equator IAU 1958
    GALEQU_TRUE = 32          # Galactic Equator (true)
    GALEQU_MULA = 33          # Galactic Equator mid-Mula
    GALALIGN_MARDYKS = 34     # Galactic alignment (Mardyks)
    TRUE_MULA = 35            # True Mula (Chandra Hari)
    GALCENT_MULA_WILHELM = 36 # Galactic Center (Mula, Wilhelm)
    ARYABHATA_522 = 37        # Aryabhata 522
    BABYLONIAN_BRITTON = 38   # Babylonian (Britton)
    
    # Modern Research Systems
    TRUE_SHEORAN = 39         # True Sheoran
    GALCENT_COCHRANE = 40     # Galactic Center (Cochrane)
    GALEQU_FIORENZA = 41      # Galactic Equator (Fiorenza)
    VALENS_MOON = 42          # Valens (Moon)
    LAHIRI_1940 = 43          # Lahiri 1940
    LAHIRI_VP285 = 44         # Lahiri VP285 (Vernal Point 285)
    KRISHNAMURTI_VP291 = 45   # Krishnamurti VP291
    LAHIRI_ICRC = 46          # Lahiri ICRC
    
    # Custom/User-defined
    USER = 255                # User-defined ayanamsa


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
