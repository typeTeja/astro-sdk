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
    VEDIC = 'V' 
    # Added explicit "Whole Sign" support if needed by code mapping
    # 'W' is SwissEph code for Whole Sign

class Planet(IntEnum):
    # Standard Swiss Ephemeris IDs
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
    LILITH_MEAN = 12  # Black Moon Lilith (Mean)
    LILITH_TRUE = 13  # True Lilith (Osculating)
    
    # Asteroids
    CHIRON = 15
    CERES = 17
    PALLAS = 18
    JUNO = 19
    VESTA = 20

class SiderealMode(IntEnum):
    """
    Sidereal Ayanamsas.
    Standardized set compatible with Swiss Ephemeris.
    """
    FAGAN_BRADLEY = 0
    LAHIRI = 1
    DELUCE = 2
    RAMAN = 3
    USHASHASHI = 4
    KRISHNAMURTI = 5
    DJWHAL_KHUL = 6
    YUKTESHWAR = 7
    JN_BHASIN = 8
    BABYLONIAN_KUGLER1 = 9
    BABYLONIAN_KUGLER2 = 10
    BABYLONIAN_KUGLER3 = 11
    BABYLONIAN_HUBER = 12
    BABYLONIAN_ETPSC = 13
    ALDEBARAN_15TAU = 14
    HIPPARCHOS = 15
    SASSANIAN = 16
    GALCENT_0SAG = 17
    J2000 = 18
    J1900 = 19
    B1950 = 20
    SURYASIDDHANTA = 21
    SURYASIDDHANTA_MSUN = 22
    ARYABHATA = 23
    ARYABHATA_MSUN = 24
    SS_REVATI = 25
    SS_CITRA = 26
    TRUE_CITRA = 27
    TRUE_REVATI = 28
    TRUE_PUSHYA = 29
    GALCENT_RGILBRAND = 30
    GALEQU_IAU1958 = 31
    GALEQU_TRUE = 32
    GALEQU_MULA = 33
    GALALIGN_MARDYKS = 34
    TRUE_MULA = 35
    GALCENT_MULA_WILHELM = 36
    ARYABHATA_522 = 37
    BABYLONIAN_BRITTON = 38
    TRUE_SHEORAN = 39
    GALCENT_COCHRANE = 40
    GALEQU_FIORENZA = 41
    VALENS_MOON = 42
    LAHIRI_1940 = 43
    LAHIRI_VP285 = 44
    KRISHNAMURTI_VP291 = 45
    LAHIRI_ICRC = 46
    USER = 255
