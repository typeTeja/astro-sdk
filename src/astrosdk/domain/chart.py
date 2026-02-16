from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from ..core.time import Time
from .planet import PlanetPosition
from .house import ChartHouses

class Chart(BaseModel):
    """Complete astrological chart with metadata."""
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    
    metadata: Dict[str, str] = Field(default_factory=dict, description="Chart metadata (name, location, etc.)")
    time: Time = Field(description="Chart time (must be timezone-aware)")
    planets: List[PlanetPosition] = Field(description="Planetary positions")
    houses: Optional[ChartHouses] = Field(None, description="House cusps and axes")
