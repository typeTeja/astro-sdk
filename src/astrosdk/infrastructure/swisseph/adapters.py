import swisseph as swe
from typing import List, Optional, Any
from astrosdk.core.time import Time
from astrosdk.core.constants import Planet, SiderealMode, HouseSystem, DEFAULT_EPHE_FLAG, ALLOWED_PLANETS
from astrosdk.core.exceptions import UnsupportedPlanetError
from astrosdk.ports.ephemeris import EphemerisProvider
from astrosdk.ports.houses import HouseProvider
from astrosdk.ports.events import EventProvider
from astrosdk.domain.models.planet import PlanetPosition, PlanetaryPhenomena, FixedStarPosition
from astrosdk.domain.models.house import ChartHouses, HouseCusp, HouseAxes
from .engine import SwissEphemerisEngine

class SwissEphemerisAdapter(EphemerisProvider, HouseProvider, EventProvider):
    """
    Concrete implementation of all ports using Swiss Ephemeris.
    Adapts Engine raw data to Domain Models.
    """
    
    def __init__(self, engine: SwissEphemerisEngine):
        self.engine = engine
        
    def _configure_calculation(
        self, 
        sidereal_mode: Optional[SiderealMode],
        heliocentric: bool,
        topocentric_coords: Optional[tuple]
    ) -> int:
        flags = DEFAULT_EPHE_FLAG | swe.FLG_SPEED
        
        if sidereal_mode is not None:
            self.engine.set_sidereal_mode(sidereal_mode)
            flags |= swe.FLG_SIDEREAL
        else:
            # Explicitly set to tropical (0) if None
            # Or assume engine default? Better to be explicit for determinism.
            # But set_sid_mode(0) is FAGAN_BRADLEY. Tropical is FAGAN_BRADLEY? No.
            # Tropical is default if SIDEREAL flag is NOT set.
            # But if a previous call set sidereal mode, does it persist?
            # Yes, swe.set_sid_mode affects global state.
            # But calc_ut only uses it if FLG_SIDEREAL is passed.
            pass
            
        if heliocentric:
            flags |= swe.FLG_HELCTR
            
        if topocentric_coords:
            self.engine.set_topocentric(*topocentric_coords)
            flags |= swe.FLG_TOPOCTR
            
        return flags

    def calculate_planet(
        self, 
        time: Time, 
        planet: Planet, 
        sidereal_mode: Optional[SiderealMode] = None,
        heliocentric: bool = False,
        topocentric_coords: Optional[tuple] = None
    ) -> PlanetPosition:
        
        if planet not in ALLOWED_PLANETS:
            raise UnsupportedPlanetError(f"Planet {planet} not allowed")

        flags = self._configure_calculation(sidereal_mode, heliocentric, topocentric_coords)
        
        res = self.engine.calculate_planet_ut(time.julian_day, planet, flags)
        
        return PlanetPosition(
            planet=planet,
            longitude=res[0],
            latitude=res[1],
            distance=res[2],
            speed_long=res[3],
            speed_lat=res[4],
            speed_dist=res[5]
        )

    def calculate_planets(
        self, 
        time: Time, 
        planets: List[Planet], 
        sidereal_mode: Optional[SiderealMode] = None,
        heliocentric: bool = False,
        topocentric_coords: Optional[tuple] = None
    ) -> List[PlanetPosition]:
        return [
            self.calculate_planet(time, p, sidereal_mode, heliocentric, topocentric_coords)
            for p in planets
        ]

    def calculate_phenomena(self, time: Time, planet: Planet) -> PlanetaryPhenomena:
        flags = DEFAULT_EPHE_FLAG
        res = self.engine.calculate_phenomena(time.julian_day, planet, flags)
        
        return PlanetaryPhenomena(
            planet=planet,
            phase_angle=res[0],
            phase_fraction=res[1],
            elongation=res[2],
            apparent_diameter=res[3],
            apparent_magnitude=res[4]
        )

    def calculate_fixed_star(
        self, 
        time: Time, 
        star_name: str, 
        sidereal_mode: Optional[SiderealMode] = None
    ) -> FixedStarPosition:
        flags = DEFAULT_EPHE_FLAG
        if sidereal_mode is not None:
            self.engine.set_sidereal_mode(sidereal_mode)
            flags |= swe.FLG_SIDEREAL
            
        res = self.engine.calculate_fixed_star(time.julian_day, star_name, flags)
        mag = self.engine.get_fixed_star_magnitude(star_name)
        
        return FixedStarPosition(
            name=star_name,
            longitude=res[0],
            latitude=res[1],
            magnitude=mag
        )

    def calculate_houses(
        self,
        time: Time,
        latitude: float,
        longitude: float,
        system: HouseSystem,
        sidereal_mode: Optional[SiderealMode] = None
    ) -> ChartHouses:
        
        if sidereal_mode is not None:
            self.engine.set_sidereal_mode(sidereal_mode)
            
        sys_byte = system.value.encode('ascii')
        
        # Calculate cusps
        # Note: swisseph.houses returns tropical cusps unless we manually subtract ayanamsa
        # BUT wait, does `swe.houses` support sidereal flag?
        # Documentation says `swe.houses` generally returns tropical.
        # If we want sidereal houses, we usually calculate tropical then subtract ayanamsa.
        
        res_cusps, res_ascmc = self.engine.calculate_houses(time.julian_day, latitude, longitude, sys_byte)
        
        ayanamsa = 0.0
        if sidereal_mode is not None:
            ayanamsa = self.engine.get_ayanamsa_ut(time.julian_day)
            
        # Normalize and apply ayanamsa
        def norm(val):
            return (val - ayanamsa) % 360.0
            
        cusps = []
        # swe.houses returns 13 elements (0 is input cusp, 1..12 are actual)
        # OR 37 elements depending on system. Assuming standard systems return 13.
        for i in range(1, 13):
            cusps.append(HouseCusp(number=i, longitude=norm(res_cusps[i])))
            
        axes = HouseAxes(
            ascendant=norm(res_ascmc[0]),
            midheaven=norm(res_ascmc[1]),
            descendant=norm((res_ascmc[0] + 180) % 360), # Approx/Simple
            imum_coeli=norm((res_ascmc[1] + 180) % 360),
            vertex=norm(res_ascmc[3])
        )
        
        return ChartHouses(
            system=system,
            cusps=cusps,
            axes=axes
        )

    def find_next_solar_eclipse(self, start_time: Time) -> Optional[Time]:
        res, tret = self.engine.search_solar_eclipse(start_time.julian_day, backward=False)
        if tret[0] == 0: return None
        return Time.from_julian_day(tret[0]) # Approximation (tret[0] is Maximum eclipse time)

    def find_next_lunar_eclipse(self, start_time: Time) -> Optional[Time]:
        res, tret = self.engine.search_lunar_eclipse(start_time.julian_day, backward=False)
        if tret[0] == 0: return None
        return Time.from_julian_day(tret[0])
