from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import Optional
from ..core.constants import Planet, ZodiacSign

class PlanetPosition(BaseModel):
    """
    Immutable planetary position with full validation.
    Represents a planet's state at a specific moment in time.
    """
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    longitude: float = Field(ge=0.0, lt=360.0, description="Ecliptic longitude in degrees")
    latitude: float = Field(ge=-90.0, le=90.0, description="Ecliptic latitude in degrees")
    distance: float = Field(ge=0.0, description="Distance from Earth/Sun in AU (0 for heliocentric Sun)")
    speed_long: float = Field(description="Longitudinal speed (degrees/day)")
    speed_lat: float = Field(description="Latitudinal speed (degrees/day)")
    speed_dist: float = Field(description="Radial speed (AU/day)")
    
    # Optional horizontal coordinates
    azimuth: Optional[float] = Field(None, ge=0.0, lt=360.0, description="Azimuth in degrees")
    altitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Altitude in degrees")
    
    @computed_field
    @property
    def sign(self) -> ZodiacSign:
        """Zodiac sign containing this position."""
        return ZodiacSign(int(self.longitude / 30))

    @computed_field
    @property
    def sign_degree(self) -> float:
        """Degree within the zodiac sign (0-30)."""
        return self.longitude % 30.0

    @computed_field
    @property
    def is_retrograde(self) -> bool:
        """True if planet is in retrograde motion."""
        return self.speed_long < 0

    @computed_field
    @property
    def antiscia(self) -> float:
        """Mirror point over Cancer/Capricorn axis."""
        return (180.0 - self.longitude) % 360.0

    @computed_field
    @property
    def contra_antiscia(self) -> float:
        """Mirror point over Aries/Libra axis."""
        return (360.0 - self.longitude) % 360.0

    @computed_field
    @property
    def zenith_distance(self) -> Optional[float]:
        """Angle from zenith (90 - altitude)."""
        return 90.0 - self.altitude if self.altitude is not None else None

class PlanetaryPhenomena(BaseModel):
    """Observable phenomena of a planetary body."""
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    phase_angle: float = Field(ge=0.0, lt=360.0, description="Angle between sun and earth as seen from planet")
    phase_fraction: float = Field(ge=0.0, le=1.0, description="Illuminated fraction of disc")
    elongation: float = Field(ge=0.0, le=180.0, description="Angular distance from sun")
    apparent_diameter: float = Field(gt=0.0, description="Apparent diameter of disc in arcseconds")
    apparent_magnitude: float = Field(description="Apparent magnitude")

class FixedStarPosition(BaseModel):
    """Position of a fixed star."""
    model_config = ConfigDict(frozen=True)
    
    name: str
    longitude: float = Field(ge=0.0, lt=360.0, description="Ecliptic longitude")
    latitude: float = Field(ge=-90.0, le=90.0, description="Ecliptic latitude")
    magnitude: float = Field(description="Apparent magnitude")
    
    @computed_field
    @property
    def sign(self) -> ZodiacSign:
        """Zodiac sign containing this star."""
        return ZodiacSign(int(self.longitude / 30))

    @computed_field
    @property
    def sign_degree(self) -> float:
        """Degree within the zodiac sign."""
        return self.longitude % 30.0
