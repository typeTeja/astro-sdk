from astrosdk.core.constants import Planet, ZodiacSign

# Default Orbs
DEFAULT_COMBUSTION_ORBS = {
    Planet.MOON: 12.0,
    Planet.MERCURY: 14.0,
    Planet.VENUS: 8.0,
    Planet.MARS: 17.0,
    Planet.JUPITER: 11.0,
    Planet.SATURN: 15.0,
    Planet.URANUS: 10.0,
    Planet.NEPTUNE: 10.0,
    Planet.PLUTO: 10.0,
}

# Default Aspect Orbs
DEFAULT_ASPECT_ORBS = {
    "CONJUNCTION": 10.0,
    "SEXTILE": 6.0,
    "SQUARE": 8.0,
    "TRINE": 8.0,
    "OPPOSITION": 10.0,
    # Minors
    "SEMI-SEXTILE": 3.0,
    "SEMI-SQUARE": 3.0,
    "SESQUI-QUADRATE": 3.0,
    "QUINCUNX": 3.0,
}

# Western Dignity Rules
WESTERN_DIGNITY_RULES = {
    Planet.SUN: {
        "exaltation": (ZodiacSign.ARIES, 19.0),
        "own_sign": [ZodiacSign.LEO],
        "detriment": [ZodiacSign.AQUARIUS],
        "fall": (ZodiacSign.LIBRA, 19.0)
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
