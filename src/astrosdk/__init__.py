"""
AstroSDK - Professional Astronomical Calculation Engine

A deterministic, precise, and type-safe SDK for astronomical calculations
powered by Swiss Ephemeris.

Quick Start:
    >>> from astrosdk import calculate_natal_chart, AstroTime
    >>> 
    >>> time = AstroTime.from_components(2000, 1, 1, 12, 0, tz="UTC")
    >>> chart = calculate_natal_chart(
    ...     time=time,
    ...     latitude=40.7128,
    ...     longitude=-74.0060
    ... )
    >>> print(chart.planets[0].longitude)  # Sun position
"""

from typing import List, Optional
from datetime import datetime, timezone

# Core imports (internal use)
from .core.ephemeris import Ephemeris as _Ephemeris
from .core.time import Time as _Time
from .core.constants import (
    Planet,
    ZodiacSign,
    HouseSystem,
    SiderealMode,
    ALLOWED_PLANETS
)

# Domain models (public)
from .domain.planet import PlanetPosition, PlanetaryPhenomena, FixedStarPosition
from .domain.house import HouseCusp, HouseAxes, ChartHouses
from .domain.aspect import Aspect
from .domain.chart import Chart

# Services (internal use)
from .services.natal_service import NatalService as _NatalService
from .services.aspect_service import AspectService as _AspectService
from .services.event_service import EventService as _EventService
from .services.crossing_service import CrossingService as _CrossingService
from .services.horizon_service import HorizonService as _HorizonService

# Internal singleton for convenience
_eph = _Ephemeris()


# ============================================================================
# Time Wrapper (Public)
# ============================================================================

class AstroTime:
    """
    Immutable, timezone-aware astronomical time.
    
    This is a convenience wrapper around the internal Time class that enforces
    strict timezone handling and provides user-friendly constructors.
    """
    
    def __init__(self, dt: datetime):
        """Create from a timezone-aware datetime."""
        if dt.tzinfo is None:
            raise ValueError("AstroTime requires timezone-aware datetime. Use from_components() or from_iso() instead.")
        self._time = _Time(dt.astimezone(timezone.utc))
    
    @classmethod
    def from_components(cls, year: int, month: int, day: int, 
                       hour: int, minute: int, second: int = 0,
                       tz: str = "UTC") -> "AstroTime":
        """
        Create AstroTime from explicit components.
        
        Args:
            year: Year (e.g., 2000)
            month: Month (1-12)
            day: Day (1-31)
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second (0-59), default 0
            tz: Timezone name (e.g., "UTC", "America/New_York")
        
        Returns:
            AstroTime instance
        """
        from zoneinfo import ZoneInfo
        dt = datetime(year, month, day, hour, minute, second, tzinfo=ZoneInfo(tz))
        return cls(dt)
    
    @classmethod
    def from_iso(cls, iso_string: str) -> "AstroTime":
        """
        Create from ISO 8601 string.
        
        Args:
            iso_string: ISO format string (e.g., "2000-01-01T12:00:00Z")
        
        Returns:
            AstroTime instance
        """
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return cls(dt)
    
    @property
    def julian_day(self) -> float:
        """Julian Day number (deterministic)."""
        return self._time.julian_day
    
    @property
    def datetime(self) -> datetime:
        """Underlying datetime (UTC)."""
        return self._time.dt
    
    def __repr__(self) -> str:
        return f"AstroTime({self._time.dt.isoformat()})"


# ============================================================================
# Public API Functions
# ============================================================================

def calculate_natal_chart(
    time: AstroTime,
    latitude: float,
    longitude: float,
    altitude: float = 0.0,
    house_system: HouseSystem = HouseSystem.PLACIDUS,
    sidereal_mode: Optional[SiderealMode] = SiderealMode.LAHIRI,
    include_horizontal: bool = False
) -> Chart:
    """
    Calculate a complete natal chart.
    
    Args:
        time: Chart time (timezone-aware)
        latitude: Observer latitude in degrees (-90 to 90)
        longitude: Observer longitude in degrees (-180 to 180)
        altitude: Observer altitude in meters (default: 0)
        house_system: House system to use (default: Placidus)
        sidereal_mode: Sidereal ayanamsa (default: Lahiri). Use None for tropical.
        include_horizontal: Include azimuth/altitude for each planet
    
    Returns:
        Complete Chart with planets and houses
    """
    service = _NatalService(_eph)
    
    # Calculate planetary positions
    planets = service.calculate_positions(
        time._time,
        sidereal_mode=sidereal_mode,
        lat=latitude if include_horizontal else None,
        lon=longitude if include_horizontal else None,
        alt=altitude
    )
    
    # Calculate houses
    houses = service.calculate_houses(
        time._time,
        latitude,
        longitude,
        system=house_system,
        sidereal_mode=sidereal_mode or SiderealMode.LAHIRI
    )
    
    return Chart(
        metadata={
            "latitude": str(latitude),
            "longitude": str(longitude),
            "house_system": house_system.name,
            "sidereal_mode": sidereal_mode.name if sidereal_mode else "TROPICAL"
        },
        time=time._time,
        planets=planets,
        houses=houses
    )


def calculate_aspects(
    positions: List[PlanetPosition],
    orbs: Optional[dict] = None,
    types: Optional[List[str]] = None
) -> List[Aspect]:
    """
    Calculate aspects between planetary positions.
    
    Args:
        positions: List of planetary positions
        orbs: Custom orb dictionary (default: standard orbs)
        types: Aspect types to calculate (default: ['major'])
            Options: 'major', 'minor', 'kepler', 'septile', 'novile', 'undecile', 'all'
    
    Returns:
        List of detected aspects
    """
    service = _AspectService()
    return service.calculate_aspects(positions, aspect_types=types, custom_orbs=orbs)


def find_next_solar_eclipse(start_time: AstroTime) -> Optional[AstroTime]:
    """
    Find the next solar eclipse.
    
    Args:
        start_time: Search start time
    
    Returns:
        AstroTime of next eclipse, or None if not found
    """
    service = _EventService(_eph)
    event = service.find_next_solar_eclipse(start_time._time)
    if event:
        # Convert Julian Day back to Time
        eclipse_time = _Time.from_julian_day(event.julian_day)
        return AstroTime(eclipse_time.dt)
    return None


def find_next_lunar_eclipse(start_time: AstroTime) -> Optional[AstroTime]:
    """
    Find the next lunar eclipse.
    
    Args:
        start_time: Search start time
    
    Returns:
        AstroTime of next eclipse, or None if not found
    """
    service = _EventService(_eph)
    event = service.find_next_lunar_eclipse(start_time._time)
    if event:
        # Convert Julian Day back to Time
        eclipse_time = _Time.from_julian_day(event.julian_day)
        return AstroTime(eclipse_time.dt)
    return None


def find_solar_return(
    natal_time: AstroTime,
    year: int,
    sidereal_mode: Optional[SiderealMode] = SiderealMode.LAHIRI
) -> AstroTime:
    """
    Find solar return for a given year.
    
    Args:
        natal_time: Natal chart time
        year: Target year for solar return
        sidereal_mode: Sidereal mode (default: Lahiri)
    
    Returns:
        AstroTime of solar return
    """
    service = _CrossingService(_eph)
    result = service.find_solar_return(natal_time._time, year, sidereal_mode=sidereal_mode)
    return AstroTime(result.dt)


def calculate_sunrise_sunset(
    time: AstroTime,
    latitude: float,
    longitude: float,
    altitude: float = 0.0
) -> dict:
    """
    Calculate sunrise and sunset times.
    
    Args:
        time: Reference time (date)
        latitude: Observer latitude
        longitude: Observer longitude  
        altitude: Observer altitude in meters
    
    Returns:
        Dictionary with 'sunrise' and 'sunset' AstroTime values
    """
    service = _HorizonService(_eph)
    rise = service.calculate_sunrise(time._time, latitude, longitude, altitude)
    set_time = service.calculate_sunset(time._time, latitude, longitude, altitude)
    
    return {
        "sunrise": AstroTime(rise.dt) if rise else None,
        "sunset": AstroTime(set_time.dt) if set_time else None
    }


# ============================================================================
# Public Exports
# ============================================================================

__all__ = [
    # Time
    "AstroTime",
    
    # Constants/Enums
    "Planet",
    "ZodiacSign",
    "HouseSystem",
    "SiderealMode",
    
    # Domain Models
    "PlanetPosition",
    "PlanetaryPhenomena",
    "FixedStarPosition",
    "HouseCusp",
    "HouseAxes",
    "ChartHouses",
    "Aspect",
    "Chart",
    
    # Public Functions
    "calculate_natal_chart",
    "calculate_aspects",
    "find_next_solar_eclipse",
    "find_next_lunar_eclipse",
    "find_solar_return",
    "calculate_sunrise_sunset",
]

__version__ = "1.3.0-dev"
