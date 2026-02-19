from typing import Optional, List
from astrosdk.core.time import Time
from astrosdk.core.constants import HouseSystem, SiderealMode
from astrosdk.domain.models.chart import Chart
from astrosdk.domain.models.planet import PlanetPosition
from astrosdk.domain.logic.combustion import calculate_combustion
from astrosdk.domain.logic.dignity import calculate_dignity
from astrosdk.ports.ephemeris import EphemerisProvider
from astrosdk.ports.houses import HouseProvider
from astrosdk.config.astro_config import AstroConfig

class NatalService:
    """
    Orchestrates the calculation of a Natal Chart.
    Uses Ports for data fetching and Domain Logic for interpretation.
    """
    
    def __init__(
        self, 
        ephemeris_provider: EphemerisProvider, 
        house_provider: HouseProvider,
        config: AstroConfig
    ):
        self.ephemeris = ephemeris_provider
        self.houses = house_provider
        self.config = config
        
    def calculate_natal_chart(
        self,
        time: Time,
        latitude: float,
        longitude: float,
        altitude: float = 0.0,
        house_system: HouseSystem = HouseSystem.PLACIDUS,
        sidereal_mode: Optional[SiderealMode] = None,
        planets: Optional[List] = None # Default list of planets could be in config
    ) -> Chart:
        
        # 1. Determine which planets to calculate
        # Should come from constants or config. 
        # For this refactor, I'll use a standard list if not provided.
        from astrosdk.core.constants import Planet, ALLOWED_PLANETS
        target_planets = planets or [p for p in ALLOWED_PLANETS if p >= 0] # Filter out negative IDs if any
        
        # 2. Fetch positions via Port
        # Note: We need to handle threading/locking in the Adapter, Service assumes safe usage.
        
        positions = self.ephemeris.calculate_planets(
            time=time,
            planets=target_planets,
            sidereal_mode=sidereal_mode,
            topocentric_coords=(latitude, longitude, altitude)
        )
        
        # 3. Calculate Houses via Port
        houses = self.houses.calculate_houses(
            time=time,
            latitude=latitude,
            longitude=longitude,
            system=house_system,
            sidereal_mode=sidereal_mode
        )
        
        # 4. Enhance positions with derived logic (Logic in Domain, orchestrated here?)
        # Actually, PlanetPosition is pure data. 
        # If we want to attach dignity/combustion, we might need a richer model or separate DTO.
        # But `Chart` model expects `List[PlanetPosition]`. 
        # If the user wants combustion, they call `combustion_service.analyze(chart)`.
        # OR we return a `NatalChart` which is an Aggregate Root that offers these methods.
        # Given `domain/chart.py` structure, it just holds data.
        
        # We return the Chart aggregate.
        
        return Chart(
            metadata={
                "latitude": str(latitude),
                "longitude": str(longitude),
                "house_system": house_system.name,
                "sidereal_mode": sidereal_mode.name if sidereal_mode else "TROPICAL"
            },
            time=time,
            planets=positions,
            houses=houses
        )
