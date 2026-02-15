from dataclasses import dataclass
from typing import List, Dict, Optional
from ..core.time import Time
from ..core.ephemeris import Ephemeris
from ..core.constants import SiderealMode, HouseSystem
from ..domain.planet import PlanetPosition
from ..domain.house import ChartHouses
from ..domain.chart import Chart
from ..services.natal_service import NatalService

class ChartEngine:
    """
    High-level API for generating full Chart objects.
    Orchestrates NatalService and any future services.
    """
    def __init__(self):
        self._ephemeris = Ephemeris()
        self._natal_service = NatalService(self._ephemeris)

    def create_chart(self, 
                     time: Time, 
                     lat: float, 
                     lon: float, 
                     system: HouseSystem = HouseSystem.PLACIDUS,
                     sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> Chart:
        """
        Generate a complete Astrological Chart.
        """
        planets = self._natal_service.calculate_positions(time, sidereal_mode)
        houses = self._natal_service.calculate_houses(time, lat, lon, system, sidereal_mode)
        
        return Chart(
            metadata={
                "sidereal_mode": sidereal_mode.name,
                "house_system": system.name,
                "lat": str(lat),
                "lon": str(lon)
            },
            time=time,
            planets=planets,
            houses=houses
        )
