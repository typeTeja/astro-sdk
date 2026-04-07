from enum import IntEnum, StrEnum
from typing import Any


class AstroEventType(StrEnum):
    """Canonical event types for all AstroEvent instances."""

    INGRESS = "INGRESS"
    STATION = "STATION"
    ASPECT = "ASPECT"
    ECLIPSE = "ECLIPSE"
    SYNODIC = "SYNODIC"
    RETURN = "RETURN"
    PARAN = "PARAN"
    HELIACAL = "HELIACAL"


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


class HouseSystem(StrEnum):
    PLACIDUS = "P"
    KOCH = "K"
    PORPHYRY = "O"
    REGIOMONTANUS = "R"
    CAMPANUS = "C"
    EQUAL = "E"
    WHOLE_SIGN = "W"
    VEDIC = "V"


def validate_enum_by_name(cls: Any, v: Any) -> Any:
    """Validator to handle name-to-value resolution for IntEnums."""
    if v is None:
        return None
    if isinstance(v, str):
        try:
            return cls[v.upper()]
        except KeyError:
            if v.isdigit():
                return cls(int(v))
            raise ValueError(f"Invalid {cls.__name__} name: {v}") from None
    elif isinstance(v, cls):
        return v
    return cls(v)


class Planet(IntEnum):
    """Swiss Ephemeris IDs for all major bodies."""

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
    MEAN_NODE = 10
    TRUE_NODE = 11
    MEAN_NODE_OPP = -1
    LILITH_MEAN = 12
    LILITH_TRUE = 13
    CHIRON = 15
    CERES = 17
    PALLAS = 18
    JUNO = 19
    VESTA = 20


class SiderealMode(IntEnum):
    """All ayanamsa systems supported by Swiss Ephemeris."""

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


EPHE_SWISSEPH = 2
EPHE_JPLEPH = 1
DEFAULT_EPHE_FLAG = EPHE_SWISSEPH
DEFAULT_TIDAL = 999999
DEFAULT_SIDEREAL = SiderealMode.LAHIRI

ALLOWED_PLANETS = {
    Planet.SUN,
    Planet.MOON,
    Planet.MERCURY,
    Planet.VENUS,
    Planet.MARS,
    Planet.JUPITER,
    Planet.SATURN,
    Planet.URANUS,
    Planet.NEPTUNE,
    Planet.PLUTO,
    Planet.TRUE_NODE,
    Planet.MEAN_NODE,
    Planet.LILITH_MEAN,
    Planet.LILITH_TRUE,
    Planet.CHIRON,
    Planet.CERES,
    Planet.PALLAS,
    Planet.JUNO,
    Planet.VESTA,
}

MAX_SEARCH_DAYS = 36525
