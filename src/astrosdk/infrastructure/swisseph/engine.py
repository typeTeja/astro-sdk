import swisseph as swe
from threading import RLock
import os
from typing import Optional, Dict, List, Tuple, Any
from astrosdk.core.constants import SiderealMode, Planet, HouseSystem, DEFAULT_EPHE_FLAG, MAX_SEARCH_DAYS
from astrosdk.core.exceptions import EphemerisError, ConfigurationError, UnsupportedPlanetError, SearchRangeTooLargeError

# Global lock for the C-extension state
_SWISS_LOCK = RLock()

class SwissEphemerisEngine:
    """
    Thread-safe wrapper around pyswisseph.
    Returns RAW data (tuples/dicts), not Domain Models.
    Responsible for locking and error handling.
    """
    
    def __init__(self, ephe_path: Optional[str] = None):
        with _SWISS_LOCK:
            self._ephe_path = ephe_path or os.environ.get("SE_EPHE_PATH", "/usr/share/libswe/ephe")
            try:
                swe.set_ephe_path(self._ephe_path)
                swe.set_tid_acc(swe.TIDAL_AUTOMATIC)
                # Default to tropical/no sidereal initially, 
                # but every calculation should explicitly set it if needed.
                swe.set_sid_mode(SiderealMode.LAHIRI, 0, 0) 
            except Exception as e:
                raise EphemerisError(f"Failed to initialize Swiss Ephemeris: {str(e)}")

    def calculate_planet_ut(
        self, 
        jd_ut: float, 
        planet: int, 
        flags: int
    ) -> tuple:
        """
        Raw calculation (UT).
        Returns (longitude, latitude, distance, speed_long, speed_lat, speed_dist).
        """
        with _SWISS_LOCK:
            try:
                # calc_ut returns ((lon, lat, dist, speed_long, speed_lat, speed_dist), flags)
                res, ret_flags = swe.calc_ut(jd_ut, planet, flags)
                return res
            except Exception as e:
                raise EphemerisError(f"Calculaton failed for planet {planet}: {str(e)}")

    def calculate_houses(
        self, 
        jd_ut: float, 
        lat: float, 
        lon: float, 
        h_sys: bytes
    ) -> tuple:
        """
        Raw house calculation.
        Returns (cusps, ascmc).
        """
        with _SWISS_LOCK:
            try:
                # returns (cusps, ascmc)
                return swe.houses(jd_ut, lat, lon, h_sys)
            except Exception as e:
                raise EphemerisError(f"House calculation failed: {str(e)}")

    def get_ayanamsa_ut(self, jd_ut: float) -> float:
        with _SWISS_LOCK:
            return swe.get_ayanamsa_ut(jd_ut)

    def set_sidereal_mode(self, mode: int, t0: float = 0.0, ayan_t0: float = 0.0):
        with _SWISS_LOCK:
            swe.set_sid_mode(mode, t0, ayan_t0)
            
    def set_topocentric(self, lon: float, lat: float, alt: float):
        with _SWISS_LOCK:
            swe.set_topo(lon, lat, alt)

    def calculate_phenomena(self, jd_ut: float, planet: int, flags: int) -> tuple:
        with _SWISS_LOCK:
            try:
                # returns (phase_angle, phase_fraction, elongation, apparent_diameter, apparent_magnitude)
                return swe.pheno_ut(jd_ut, planet, flags)
            except Exception as e:
                raise EphemerisError(f"Phenomena calculation failed: {str(e)}")

    def calculate_fixed_star(self, jd_ut: float, star_name: str, flags: int) -> tuple:
        with _SWISS_LOCK:
            try:
                # returns ((lon, lat, dist, ...), name)
                res = swe.fixstar_ut(star_name, jd_ut, flags)
                xx = res[0]
                return xx
            except Exception as e:
                raise EphemerisError(f"Star calculation failed: {str(e)}")
                
    def get_fixed_star_magnitude(self, star_name: str) -> float:
        with _SWISS_LOCK:
            try:
                # returns (mag, ...)
                res = swe.fixstar_mag(star_name)
                if isinstance(res, tuple):
                    return res[0]
                return res
            except Exception as e:
                # Magnitude lookup might fail if star not found in data
                return 0.0

    def search_solar_eclipse(self, jd_start: float, backward: bool) -> tuple:
        with _SWISS_LOCK:
            try:
                # returns (ret_list, tret)
                # tret[0] is time of maximum
                res, tret = swe.sol_eclipse_when_glob(jd_start, DEFAULT_EPHE_FLAG, 0, backward)
                return res, tret
            except Exception as e:
                raise EphemerisError(f"Solar eclipse search failed: {str(e)}")

    def search_lunar_eclipse(self, jd_start: float, backward: bool) -> tuple:
        with _SWISS_LOCK:
            try:
                res, tret = swe.lun_eclipse_when(jd_start, DEFAULT_EPHE_FLAG, 0, backward)
                return res, tret
            except Exception as e:
                raise EphemerisError(f"Lunar eclipse search failed: {str(e)}")
