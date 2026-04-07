from ..core.constants import HouseSystem, SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.chart import Chart
from ..services.natal_service import NatalService


class ChartEngine:
    """
    High-level API for generating full Chart objects.
    Orchestrates NatalService and any future services.
    """

    def __init__(self) -> None:
        self._ephemeris = Ephemeris()
        self._natal_service = NatalService(self._ephemeris)

    def create_chart(
        self,
        time: Time,
        lat: float,
        lon: float,
        system: HouseSystem = HouseSystem.PLACIDUS,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
        is_sidereal: bool = True,
    ) -> Chart:
        """
        Generate a complete Astrological Chart.
        """
        # Pass None to signal Tropical Mode
        mode_for_calc = sidereal_mode if is_sidereal else None
        
        planets = self._natal_service.calculate_positions(
            time=time, 
            sidereal_mode=mode_for_calc, 
            is_sidereal=is_sidereal
        )
        houses = self._natal_service.calculate_houses(
            time=time, 
            lat=lat, 
            lon=lon, 
            system=system, 
            sidereal_mode=sidereal_mode, 
            is_sidereal=is_sidereal
        )

        return Chart(
            metadata={
                "sidereal_mode": sidereal_mode.name,
                "house_system": system.name,
                "lat": str(lat),
                "lon": str(lon),
            },
            time=time,
            planets=planets,
            houses=houses,
        )
