from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from astrosdk.core.time import Time
from .planet import PlanetPosition
from .house import ChartHouses

class Chart(BaseModel):
    """Complete astrological chart with metadata."""
    model_config = ConfigDict(frozen=True)
    
    metadata: Dict[str, str] = Field(default_factory=dict)
    time: Time
    planets: List[PlanetPosition]
    houses: Optional[ChartHouses] = None
