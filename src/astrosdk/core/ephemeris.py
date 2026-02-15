import swisseph as swe
from threading import RLock
from typing import Optional, Dict, Set
import os
from dotenv import load_dotenv, find_dotenv
from .constants import SiderealMode, Planet, HouseSystem, DEFAULT_EPHE_FLAG, ALLOWED_PLANETS, MAX_SEARCH_DAYS
from .errors import EphemerisError, ConfigurationError, UnsupportedPlanetError, InvalidTimeStandardError, SearchRangeTooLargeError

# Global library-level lock to protect the shared mutable state of pyswisseph
_SWISS_LOCK = RLock()

class Ephemeris:
    """
    Singleton-style wrapper for Swiss Ephemeris.
    Ensures thread safety and consistent core policy enforcement.
    """
    _instance = None
    _lock = RLock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Ephemeris, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        with _SWISS_LOCK:
            self._sidereal_mode = SiderealMode.LAHIRI
            
            # Load environment variables from .env if present
            load_dotenv(find_dotenv())
            
            self._ephe_path = os.getenv("SE_EPHE_PATH", "/usr/share/libswe/ephe")
            
            # Initialize SwissEph
            try:
                swe.set_ephe_path(self._ephe_path)
                # Set default sidereal mode
                swe.set_sid_mode(self._sidereal_mode, 0, 0)
                # Ensure tidy acceleration is automatic (DE431)
                swe.set_tid_acc(swe.TIDAL_AUTOMATIC)
            except Exception as e:
                raise EphemerisError(f"Failed to initialize Swiss Ephemeris: {str(e)}")
            
        self._initialized = True

    def set_sidereal_mode(self, mode: SiderealMode, t0: float = 0.0, ayan_t0: float = 0.0):
        """
        Explicitly set the sidereal mode. Protected by global lock.
        """
        with _SWISS_LOCK:
            self._sidereal_mode = mode
            swe.set_sid_mode(mode, t0, ayan_t0)

    def calculate_planet(self, jd: float, planet: Planet, sidereal: bool = True) -> Dict[str, float]:
        """
        Calculate planet position.
        :param jd: Julian Day (UT) - ET is calculated internally.
        """
        if planet not in ALLOWED_PLANETS:
            raise UnsupportedPlanetError(f"Planet ID {planet} is not in the allowed list for this engine.")

        flags = DEFAULT_EPHE_FLAG | swe.FLG_SPEED
        if sidereal:
            flags |= swe.FLG_SIDEREAL
            
        with _SWISS_LOCK:
            try:
                xx, ret_flags = swe.calc_ut(jd, planet, flags)
                
                return {
                    "longitude": xx[0],
                    "latitude": xx[1],
                    "distance": xx[2],
                    "speed_long": xx[3],
                    "speed_lat": xx[4],
                    "speed_dist": xx[5]
                }
            except Exception as e:
                raise EphemerisError(f"Calculation failed for planet {planet}: {str(e)}")

    def calculate_houses(self, jd: float, lat: float, lon: float, system: HouseSystem = HouseSystem.PLACIDUS, sidereal: bool = True):
        """
        Calculate house cusps and ascendant. Protected by global lock.
        """
        with _SWISS_LOCK:
            try:
                h_sys_code = system.value.encode('ascii')
                cusps, ascmc = swe.houses(jd, lat, lon, h_sys_code)
                
                ayanamsa = 0.0
                if sidereal:
                    ayanamsa = swe.get_ayanamsa_ut(jd)
                    
                return {
                    "cusps": [c - ayanamsa for c in cusps],
                    "ascendant": ascmc[0] - ayanamsa,
                    "mc": ascmc[1] - ayanamsa,
                    "armc": ascmc[2],
                    "vertex": ascmc[3] - ayanamsa
                }
            except Exception as e:
                raise EphemerisError(f"House calculation failed: {str(e)}")

    def set_topocentric(self, lat: float, lon: float, alt: float):
        """
        Set topocentric parameters. Protected by global lock.
        """
        with _SWISS_LOCK:
            swe.set_topo(lon, lat, alt)

    def calculate_phenomena(self, jd: float, planet: Planet) -> Dict[str, float]:
        """
        Calculate planetary phenomena.
        """
        if planet not in ALLOWED_PLANETS:
             raise UnsupportedPlanetError(f"Planet ID {planet} is not allowed.")

        with _SWISS_LOCK:
            try:
                attr = swe.pheno_ut(jd, planet, DEFAULT_EPHE_FLAG)
                return {
                    "phase_angle": attr[0],
                    "phase_fraction": attr[1],
                    "elongation": attr[2],
                    "apparent_diameter": attr[3],
                    "apparent_magnitude": attr[4]
                }
            except Exception as e:
                raise EphemerisError(f"Phenomena calculation failed for planet {planet}: {str(e)}")

    def calculate_fixed_star(self, jd: float, star_name: str, sidereal: bool = True) -> Dict[str, float]:
        """
        Calculate fixed star position.
        """
        flags = DEFAULT_EPHE_FLAG
        if sidereal:
            flags |= swe.FLG_SIDEREAL
            
        # Enterprise Hardening: Verify star file existence
        # Fixed stars usually reside in fixstars.cat or sefstars.txt
        star_files = ["sefstars.txt", "fixstars.cat"]
        found = False
        for sf in star_files:
            if os.path.exists(os.path.join(self._ephe_path, sf)):
                found = True
                break
        if not found:
            raise ConfigurationError(f"Required star catalog file ({star_files}) not found in {self._ephe_path}")

        with _SWISS_LOCK:
            try:
                res = swe.fixstar_ut(star_name, jd, flags)
                xx = res[0]
                name = res[1]
                
                res_mag = swe.fixstar_mag(star_name)
                mag = res_mag[0] if isinstance(res_mag, (tuple, list)) else res_mag
                
                return {
                    "name": name,
                    "longitude": xx[0],
                    "latitude": xx[1],
                    "magnitude": mag
                }
            except Exception as e:
                raise EphemerisError(f"Fixed star calculation failed for {star_name}: {str(e)}")

    def get_sidereal_time(self, jd: float) -> float:
        """
        Calculate Greenwich Mean Sidereal Time.
        """
        with _SWISS_LOCK:
            return swe.sidtime(jd)

    def search_solar_eclipse(self, jd_start: float, jd_end: Optional[float] = None, backward: bool = False):
        """
        Find next/previous solar eclipse globally.
        
        :param jd_start: Starting Julian Day (UT)
        :param jd_end: Optional ending Julian Day (UT) for range validation
        :param backward: If True, search backward in time
        :raises SearchRangeTooLargeError: If search range exceeds MAX_SEARCH_DAYS
        """
        # Enforce search range limit if end date provided
        if jd_end is not None:
            search_range = abs(jd_end - jd_start)
            if search_range > MAX_SEARCH_DAYS:
                raise SearchRangeTooLargeError(
                    f"Search range of {search_range:.0f} days exceeds maximum allowed "
                    f"({MAX_SEARCH_DAYS} days / ~{MAX_SEARCH_DAYS/365.25:.0f} years)"
                )
        
        with _SWISS_LOCK:
            try:
                res, tret = swe.sol_eclipse_when_glob(jd_start, DEFAULT_EPHE_FLAG, 0, backward)
                return {
                    "peak_jd": tret[0],
                    "magnitude": 1.0, 
                    "type": res
                }
            except Exception as e:
                raise EphemerisError(f"Solar eclipse search failed: {str(e)}")

    def search_lunar_eclipse(self, jd_start: float, jd_end: Optional[float] = None, backward: bool = False):
        """
        Find next lunar eclipse globally.
        
        :param jd_start: Starting Julian Day (UT)
        :param jd_end: Optional ending Julian Day (UT) for range validation
        :param backward: If True, search backward in time
        :raises SearchRangeTooLargeError: If search range exceeds MAX_SEARCH_DAYS
        """
        # Enforce search range limit if end date provided
        if jd_end is not None:
            search_range = abs(jd_end - jd_start)
            if search_range > MAX_SEARCH_DAYS:
                raise SearchRangeTooLargeError(
                    f"Search range of {search_range:.0f} days exceeds maximum allowed "
                    f"({MAX_SEARCH_DAYS} days / ~{MAX_SEARCH_DAYS/365.25:.0f} years)"
                )
        
        with _SWISS_LOCK:
            try:
                res, tret = swe.lun_eclipse_when(jd_start, DEFAULT_EPHE_FLAG, 0, backward)
                return {
                    "peak_jd": tret[0],
                    "magnitude": 1.0,
                    "type": res
                }
            except Exception as e:
                raise EphemerisError(f"Lunar eclipse search failed: {str(e)}")
