from typing import Any

from app.core.constants import DEFAULT_EPHE_FLAG, DEFAULT_SIDEREAL
from app.core.ephemeris import Ephemeris


def get_engine_metadata() -> dict[str, Any]:
    """
    Expose runtime environment and engine configuration.
    """
    runtime = Ephemeris().get_runtime_metadata()
    return {
        "pyswisseph_version": runtime["pyswisseph_version"],
        "de_number": runtime["de_number"],
        "tidal_acceleration": runtime["tidal_acceleration"],
        "ephemeris_path": runtime["ephemeris_path"],
        "sidereal_default": DEFAULT_SIDEREAL.name,
        "sidereal_mode": runtime["sidereal_mode"],
        "topocentric": runtime["topocentric"],
        "default_ephemeris": ("Swiss Ephemeris" if DEFAULT_EPHE_FLAG == 2 else "JPL Ephemeris"),
        "starfile": "fixstars.cat",  # Swiss default
    }
