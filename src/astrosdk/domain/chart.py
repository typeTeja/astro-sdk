from dataclasses import dataclass
from typing import List, Dict, Optional
from ..core.time import Time
from .planet import PlanetPosition
from .house import ChartHouses

@dataclass(frozen=True)
class Chart:
    metadata: Dict[str, str]
    time: Time
    planets: List[PlanetPosition]
    houses: Optional[ChartHouses] = None
