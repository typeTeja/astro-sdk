from ..contexts import build_western_chart_context
from ..core.constants import HouseSystem, SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.chart import Chart
from ..services.western import WesternChartService


class ChartEngine:
    """
    High-level API for generating full Chart objects.
    Orchestrates NatalService and any future services.
    """

    def __init__(self) -> None:
        self._ephemeris = Ephemeris()

    def create_chart(
        self,
        time: Time,
        lat: float,
        lon: float,
        system: HouseSystem = HouseSystem.PLACIDUS,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
        is_sidereal: bool = True,
        heliocentric: bool = False,
    ) -> Chart:
        """
        Generate a complete Astrological Chart.
        """
        context = build_western_chart_context(
            house_system=system,
            sidereal_mode=sidereal_mode,
            is_sidereal=is_sidereal,
            heliocentric=heliocentric,
            latitude=lat,
            longitude=lon,
        )
        chart_service = WesternChartService(context, ephemeris=self._ephemeris)
        return chart_service.create_chart(time, lat, lon)
