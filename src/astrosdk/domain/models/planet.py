from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import Optional
from astrosdk.core.constants import Planet, ZodiacSign

class PlanetPosition(BaseModel):
    """
    Immutable planetary position DTO.
    Pure data. NO logic methods (calculate_combustion, etc.) to keep it clean.
    Use Domain Services for calculations.
    """
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    longitude: float = Field(ge=0.0, lt=360.0)
    latitude: float = Field(ge=-90.0, le=90.0)
    distance: float = Field(ge=0.0)
    speed_long: float
    speed_lat: float
    speed_dist: float
    
    # Horizontal coordinates (Optional)
    azimuth: Optional[float] = None
    altitude: Optional[float] = None
    
    @computed_field
    @property
    def sign(self) -> ZodiacSign:
        return ZodiacSign(int(self.longitude / 30))

    @computed_field
    @property
    def sign_degree(self) -> float:
        return self.longitude % 30.0

    @computed_field
    @property
    def is_retrograde(self) -> bool:
        return self.speed_long < 0

class PlanetaryPhenomena(BaseModel):
    """Observable phenomena of a planetary body."""
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    phase_angle: float
    phase_fraction: float
    elongation: float
    apparent_diameter: float
    apparent_magnitude: float

class FixedStarPosition(BaseModel):
    """Position of a fixed star."""
    model_config = ConfigDict(frozen=True)
    
    name: str
    longitude: float = Field(ge=0.0, lt=360.0)
    latitude: float = Field(ge=-90.0, le=90.0)
    magnitude: float
    
    @computed_field
    @property
    def sign(self) -> ZodiacSign:
        return ZodiacSign(int(self.longitude / 30))

    @computed_field
    @property
    def sign_degree(self) -> float:
        return self.longitude % 30.0
