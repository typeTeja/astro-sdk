from dataclasses import dataclass
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
    
    @property
    def sign(self) -> ZodiacSign:
        return ZodiacSign(int(self.longitude / 30))

    @property
    def sign_degree(self) -> float:
        return self.longitude % 30.0

    @property
    def is_retrograde(self) -> bool:
        return self.speed_long < 0
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
