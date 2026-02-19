from typing import Protocol, Optional
from astrosdk.core.time import Time
from astrosdk.core.constants import HouseSystem, SiderealMode
from astrosdk.domain.models.house import ChartHouses

class HouseProvider(Protocol):
    """
    Abstract interface for house system calculations.
    """
    
    def calculate_houses(
        self,
        time: Time,
        latitude: float,
        longitude: float,
        system: HouseSystem,
        sidereal_mode: Optional[SiderealMode] = None
    ) -> ChartHouses:
        """
        Calculate house cusps and axes.
        Should handle fallbacks internally or raise explicit errors?
        v2.md says "Remove magic fallbacks". So this should likely raise or let the adapter decide policy.
        """
        ...
