from app.contexts import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.western.chart import WesternChart
from app.services.astronomy.planetary_service import AstronomyPlanetaryService
from app.services.astronomy.house_service import AstronomyHouseService
from app.domain.common.metadata import DomainMetadata


class WesternChartService:
    """AstroSDK 2.0 service for Western chart generation."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._planetary_service = AstronomyPlanetaryService(self.context, self._ephemeris)
        self._house_service = AstronomyHouseService(self.context, self._ephemeris)

    def create_chart(self, time: Time, lat: float, lon: float) -> WesternChart:
        """Creates a fully namespaced WesternChart."""
        planets = self._planetary_service.calculate_positions(time=time)
        houses = self._house_service.calculate_houses(time=time, lat=lat, lon=lon)

        return WesternChart(
            time=time.dt,
            planets=tuple(planets),
            metadata=DomainMetadata(
                capability=self.context.feature.capability,
                maturity=self.context.feature.maturity.value,
                fingerprint=self.context.fingerprint
            )
        )
