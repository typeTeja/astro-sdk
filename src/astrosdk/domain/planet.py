from dataclasses import dataclass
from typing import Optional
from ..core.constants import Planet, ZodiacSign

@dataclass(frozen=True)
class PlanetPosition:
    planet: Planet
    longitude: float
    latitude: float
    distance: float
    speed_long: float
    speed_lat: float
    speed_dist: float
    # Local horizontal coordinates (optional)
    azimuth: Optional[float] = None
    altitude: Optional[float] = None
    
    @property
    def sign(self) -> ZodiacSign:
        return ZodiacSign(int(self.longitude / 30))

    @property
    def sign_degree(self) -> float:
        return self.longitude % 30.0

    @property
    def is_retrograde(self) -> bool:
        return self.speed_long < 0

    @property
    def antiscia(self) -> float:
        """Mirror point over Cancer/Capricorn axis."""
        return (180.0 - self.longitude) % 360.0

    @property
    def contra_antiscia(self) -> float:
        """Mirror point over Aries/Libra axis."""
        return (360.0 - self.longitude) % 360.0

    @property
    def zenith_distance(self) -> Optional[float]:
        """Angle from zenith (90 - altitude)."""
        return 90.0 - self.altitude if self.altitude is not None else None
@dataclass(frozen=True)
class PlanetaryPhenomena:
    planet: Planet
    phase_angle: float        # angle between sun and earth as seen from planet
    phase_fraction: float     # illuminated fraction of disc
    elongation: float         # angular distance from sun
    apparent_diameter: float  # apparent diameter of disc
    apparent_magnitude: float # apparent magnitude

@dataclass(frozen=True)
class FixedStarPosition:
    name: str
    longitude: float
    latitude: float
    magnitude: float
    
    @property
    def sign(self) -> ZodiacSign:
        return ZodiacSign(int(self.longitude / 30))

    @property
    def sign_degree(self) -> float:
        return self.longitude % 30.0
