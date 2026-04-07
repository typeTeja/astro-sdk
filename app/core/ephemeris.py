import os
from functools import lru_cache
from threading import RLock
from typing import Any

import swisseph as swe
from dotenv import find_dotenv, load_dotenv

from .constants import (
    ALLOWED_PLANETS,
    DEFAULT_EPHE_FLAG,
    MAX_SEARCH_DAYS,
    HouseSystem,
    Planet,
    SiderealMode,
)
from .errors import (
    ConfigurationError,
    EphemerisError,
    SearchRangeTooLargeError,
    UnsupportedPlanetError,
)

# Global library-level lock to protect the shared mutable state of pyswisseph
_SWISS_LOCK = RLock()


class Ephemeris:
    """
    Singleton-style wrapper for Swiss Ephemeris.
    Ensures thread safety and consistent core policy enforcement.
    """

    _instance = None
    _lock = RLock()

    def __new__(cls) -> "Ephemeris":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    _initialized: bool

    def __init__(self) -> None:
        if self._initialized:
            return

        with _SWISS_LOCK:
            self._sidereal_mode = SiderealMode.LAHIRI

            # Load environment variables from .env if present
            load_dotenv(find_dotenv())

            # Set default path relative to the app package for portability
            pkg_dir = os.path.dirname(os.path.dirname(__file__))
            default_ephe_path = os.path.join(pkg_dir, "resources", "ephe")
            self._ephe_path = os.getenv("SE_EPHE_PATH", default_ephe_path)

            # Initialize SwissEph
            try:
                swe.set_ephe_path(self._ephe_path)
                # Set default sidereal mode
                swe.set_sid_mode(self._sidereal_mode, 0, 0)
                # Ensure tidy acceleration is automatic (DE431)
                swe.set_tid_acc(swe.TIDAL_AUTOMATIC)
            except Exception as e:
                raise EphemerisError(f"Failed to initialize Swiss Ephemeris: {str(e)}") from e

        self._initialized = True

    @property
    def ephe_path(self) -> str:
        """Get the current ephemeris data path."""
        return self._ephe_path

    def set_sidereal_mode(self, mode: SiderealMode, t0: float = 0.0, ayan_t0: float = 0.0) -> None:
        """
        Explicitly set the sidereal mode. Protected by global lock.
        """
        with _SWISS_LOCK:
            self._sidereal_mode = mode
            swe.set_sid_mode(mode, t0, ayan_t0)

    def calculate_planet(
        self, jd: float, planet: Planet, sidereal: bool = True, heliocentric: bool = False
    ) -> dict[str, float]:
        """
        Calculate planet position.
        """
        if planet not in ALLOWED_PLANETS:
            raise UnsupportedPlanetError(
                f"Planet ID {planet} is not in the allowed list for this engine."
            )

        flags = DEFAULT_EPHE_FLAG | swe.FLG_SPEED
        if sidereal:
            flags |= swe.FLG_SIDEREAL
        if heliocentric:
            flags |= swe.FLG_HELCTR  # Heliocentric flag

        with _SWISS_LOCK:
            try:
                xx, ret_flags = swe.calc_ut(jd, planet, flags)

                return {
                    "longitude": xx[0],
                    "latitude": xx[1],
                    "distance": xx[2],
                    "speed_long": xx[3],
                    "speed_lat": xx[4],
                    "speed_dist": xx[5],
                }
            except Exception as e:
                raise EphemerisError(f"Calculation failed for planet {planet}: {str(e)}") from e

    def calculate_houses(
        self,
        jd: float,
        lat: float,
        lon: float,
        system: HouseSystem = HouseSystem.PLACIDUS,
        sidereal: bool = True,
    ) -> dict[str, Any]:
        """
        Calculate house cusps and ascendant. Protected by global lock.
        """
        with _SWISS_LOCK:
            try:
                h_sys_code = system.value.encode("ascii")
                cusps, ascmc = swe.houses(jd, lat, lon, h_sys_code)

                ayanamsa = 0.0
                if sidereal:
                    ayanamsa = swe.get_ayanamsa_ut(jd)

                return {
                    "cusps": [c - ayanamsa for c in cusps],
                    "ascendant": ascmc[0] - ayanamsa,
                    "mc": ascmc[1] - ayanamsa,
                    "armc": ascmc[2],
                    "vertex": ascmc[3] - ayanamsa,
                }
            except Exception as e:
                raise EphemerisError(f"House calculation failed: {str(e)}") from e

    def set_topocentric(self, lat: float, lon: float, alt: float) -> None:
        """
        Set topocentric parameters. Protected by global lock.
        """
        with _SWISS_LOCK:
            swe.set_topo(lon, lat, alt)

    def calculate_phenomena(self, jd: float, planet: Planet) -> dict[str, float]:
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
                    "apparent_magnitude": attr[4],
                }
            except Exception as e:
                raise EphemerisError(
                    f"Phenomena calculation failed for planet {planet}: {str(e)}"
                ) from e

    def calculate_fixed_star(
        self, jd: float, star_name: str, sidereal: bool = True
    ) -> dict[str, Any]:
        """
        Calculate fixed star position.
        """
        flags = DEFAULT_EPHE_FLAG
        if sidereal:
            flags |= swe.FLG_SIDEREAL

        # Enterprise Hardening: Verify star file existence
        star_files = ["sefstars.txt", "fixstars.cat"]
        found = False
        for sf in star_files:
            if os.path.exists(os.path.join(self._ephe_path, sf)):
                found = True
                break
        if not found:
            raise ConfigurationError(
                f"Required star catalog file ({star_files}) not found in {self._ephe_path}"
            )

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
                    "magnitude": mag,
                }
            except Exception as e:
                raise EphemerisError(
                    f"Fixed star calculation failed for {star_name}: {str(e)}"
                ) from e

    def get_sidereal_time(self, jd: float) -> float:
        """
        Calculate Greenwich Mean Sidereal Time.
        """
        with _SWISS_LOCK:
            return float(swe.sidtime(jd))

    def search_solar_eclipse(
        self, jd_start: float, jd_end: float | None = None, backward: bool = False
    ) -> dict[str, Any]:
        """
        Find next/previous solar eclipse globally.
        """
        if jd_end is not None:
            search_range = abs(jd_end - jd_start)
            if search_range > MAX_SEARCH_DAYS:
                raise SearchRangeTooLargeError(
                    f"Search range of {search_range:.0f} days exceeds maximum allowed "
                    f"({MAX_SEARCH_DAYS} days)"
                )

        _SOLAR_ECLIPSE_TYPE: dict[int, str] = {
            1: "TOTAL",
            2: "ANNULAR",
            4: "HYBRID",
            8: "PARTIAL",
        }

        with _SWISS_LOCK:
            try:
                res = swe.sol_eclipse_when_glob(jd_start, DEFAULT_EPHE_FLAG, 0, backward)
                # res[0] = bitmask flag; res[1] = tret array
                # tret[0] = peak JD, tret[1] = umbral magnitude
                ec_flag = int(res[0]) & 0xF
                tret = res[1]
                return {
                    "peak_jd": float(tret[0]),
                    "magnitude": float(tret[1]),
                    "type": _SOLAR_ECLIPSE_TYPE.get(ec_flag, f"UNKNOWN({ec_flag})"),
                }
            except Exception as e:
                raise EphemerisError(f"Solar eclipse search failed: {str(e)}") from e

    def search_lunar_eclipse(
        self, jd_start: float, jd_end: float | None = None, backward: bool = False
    ) -> dict[str, Any]:
        """
        Find next lunar eclipse globally.
        """
        if jd_end is not None:
            search_range = abs(jd_end - jd_start)
            if search_range > MAX_SEARCH_DAYS:
                raise SearchRangeTooLargeError("Search range error")

        _LUNAR_ECLIPSE_TYPE: dict[int, str] = {
            1: "TOTAL",
            2: "PARTIAL",
            4: "PENUMBRAL",
        }

        with _SWISS_LOCK:
            try:
                res = swe.lun_eclipse_when(jd_start, DEFAULT_EPHE_FLAG, 0, backward)
                # res[0] = bitmask; res[1] = tret array
                # tret[0] = peak JD, tret[1] = umbral magnitude
                ec_flag = int(res[0]) & 0xF
                tret = res[1]
                return {
                    "peak_jd": float(tret[0]),
                    "magnitude": float(tret[1]),
                    "type": _LUNAR_ECLIPSE_TYPE.get(ec_flag, f"UNKNOWN({ec_flag})"),
                }
            except Exception as e:
                raise EphemerisError(f"Lunar eclipse search failed: {str(e)}") from e

    def find_next_eclipse(self, jd_start: float, solar: bool = True) -> dict[str, Any]:
        """
        Unified wrapper for eclipse searching. Resolve API mapping violations.
        """
        if solar:
            return self.search_solar_eclipse(jd_start)
        return self.search_lunar_eclipse(jd_start)

    def calculate_nodes_and_apsides(self, jd: float, planet: Planet) -> dict[str, dict[str, float]]:
        """
        Calculate planetary nodes and apsides.
        """
        with _SWISS_LOCK:
            try:
                res = swe.nod_aps_ut(jd, planet, DEFAULT_EPHE_FLAG, 0)

                return {
                    "ascending_node": {
                        "longitude": res[0][0],
                        "latitude": res[0][1],
                        "distance": res[0][2],
                    },
                    "descending_node": {
                        "longitude": res[1][0],
                        "latitude": res[1][1],
                        "distance": res[1][2],
                    },
                    "perihelion": {
                        "longitude": res[2][0],
                        "latitude": res[2][1],
                        "distance": res[2][2],
                    },
                    "aphelion": {
                        "longitude": res[3][0],
                        "latitude": res[3][1],
                        "distance": res[3][2],
                    },
                }
            except Exception as e:
                raise EphemerisError(
                    f"Nodes and apsides calculation failed for {planet}: {str(e)}"
                ) from e

    def calculate_rise_set(
        self,
        jd: float,
        planet: Planet,
        lat: float,
        lon: float,
        alt: float = 0.0,
        atpress: float = 1013.25,
        attemp: float = 15.0,
        is_rise: bool = True,
        rsmi_extra: int = 0,
    ) -> float | None:
        """
        Calculate rise or set time for a planet.
        """
        flags = DEFAULT_EPHE_FLAG
        rsmi = swe.CALC_RISE if is_rise else swe.CALC_SET
        rsmi |= rsmi_extra

        geopos = (lon, lat, alt)

        with _SWISS_LOCK:
            try:
                status, tret = swe.rise_trans(jd, int(planet), rsmi, geopos, atpress, attemp, flags)
                return float(tret[0]) if status == 0 else None
            except Exception as e:
                event = "rise" if is_rise else "set"
                raise EphemerisError(f"Failed to calculate {event} for {planet}: {str(e)}") from e

    def calculate_transit(
        self, jd: float, planet: Planet, lat: float, lon: float, alt: float = 0.0
    ) -> float | None:
        """
        Calculate meridian transit (culmination) time.
        """
        flags = DEFAULT_EPHE_FLAG
        rsmi = swe.CALC_MTRANSIT
        geopos = (lon, lat, alt)

        with _SWISS_LOCK:
            try:
                status, tret = swe.rise_trans(jd, int(planet), rsmi, geopos, 0, 0, flags)
                return float(tret[0]) if status == 0 else None
            except Exception as e:
                raise EphemerisError(f"Failed to calculate transit for {planet}: {str(e)}") from e

    def calculate_horizontal(
        self,
        jd: float,
        lon_ecl: float,
        lat_ecl: float,
        dist: float,
        lat: float,
        lon: float,
        alt: float = 0.0,
        atpress: float = 1013.25,
        attemp: float = 15.0,
    ) -> dict[str, float]:
        """
        Convert ecliptic coordinates to horizontal (Azimuth/Altitude).
        """
        geopos = (lon, lat, alt)
        xin = (lon_ecl, lat_ecl, dist)

        with _SWISS_LOCK:
            try:
                res = swe.azalt(jd, swe.ECL2HOR, geopos, atpress, attemp, xin)
                return {
                    "azimuth": res[0],
                    "true_altitude": res[1],
                    "apparent_altitude": res[2],
                }
            except Exception as e:
                raise EphemerisError(f"Horizontal conversion failed: {str(e)}") from e

    def calculate_heliacal_event(
        self,
        jd: float,
        planet: Planet,
        lat: float,
        lon: float,
        alt: float = 0.0,
        pressure: float = 1013.25,
        temperature: float = 15.0,
        humidity: float = 50.0,
        extinction: float = 0.0,
        event_type: int = 1,  # 1 = Heliacal Rising
        star_name: str = "",
    ) -> dict[str, float]:
        """
        Calculate the next heliacal phenomenon.
        """
        geopos = (lon, lat, alt)
        datm = (pressure, temperature, humidity, extinction)
        dobs = (30, 1.0, 0, 0, 0, 0)
        flags = swe.FLG_SWIEPH

        planet_names = {
            Planet.MERCURY: "Mercury",
            Planet.VENUS: "Venus",
            Planet.MARS: "Mars",
            Planet.JUPITER: "Jupiter",
            Planet.SATURN: "Saturn",
            Planet.URANUS: "Uranus",
            Planet.NEPTUNE: "Neptune",
            Planet.PLUTO: "Pluto",
            Planet.MOON: "Moon",
        }

        body_name = star_name if star_name else planet_names.get(planet, "")
        if not body_name:
            raise EphemerisError(
                f"Heliacal calculation requires a name. Planet {planet} not mapped."
            )

        with _SWISS_LOCK:
            try:
                res = swe.heliacal_ut(jd, geopos, datm, dobs, body_name, event_type, flags)
                status, tret, dret = res
                if status == 0:
                    return {
                        "event_jd": tret[0],
                        "alt_sun": dret[0],
                        "alt_body": dret[1],
                        "visibility_duration": dret[2],
                    }
                return {}
            except Exception as e:
                raise EphemerisError(
                    f"Heliacal calculation failed for {body_name}: {str(e)}"
                ) from e

    def calculate_stationary_point(
        self,
        jd_start: float,
        planet: Planet,
        forward: bool = True,
        max_days: float = 180.0,
    ) -> float | None:
        """
        Find the next stationary point (speed_long == 0).
        """
        if planet not in ALLOWED_PLANETS or planet in [Planet.SUN, Planet.MOON]:
            return None

        step = 1.0 if forward else -1.0
        current_jd = jd_start
        last_speed = self.calculate_planet(current_jd, planet)["speed_long"]
        found = False

        for _ in range(int(max_days)):
            current_jd += step
            current_data = self.calculate_planet(current_jd, planet)
            current_speed = current_data["speed_long"]

            if last_speed * current_speed <= 0:
                found = True
                break
            last_speed = current_speed

        if not found:
            return None

        t1 = current_jd - step
        t2 = current_jd

        for _ in range(20):
            tm = (t1 + t2) / 2.0
            sm = self.calculate_planet(tm, planet)["speed_long"]

            if last_speed * sm <= 0:
                t2 = tm
            else:
                t1 = tm
                last_speed = sm

        return (t1 + t2) / 2.0
