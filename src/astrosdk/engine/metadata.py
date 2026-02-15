import swisseph as swe
from ..core.constants import DEFAULT_SIDEREAL, DEFAULT_EPHE_FLAG

def get_engine_metadata():
    """
    Expose runtime environment and engine configuration.
    """
    return {
        "pyswisseph_version": swe.version(),
        "de_number": swe.DE_NUMBER,
        "tidal_acceleration": swe.get_tid_acc(),
        "ephemeris_path": swe.get_library_path(),
        "sidereal_default": DEFAULT_SIDEREAL.name,
        "default_ephemeris": "Swiss Ephemeris" if DEFAULT_EPHE_FLAG == 2 else "JPL Ephemeris",
        "starfile": "fixstars.cat" # Swiss default
    }
