from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.services.astronomy.crossing_service import AstronomyCrossingService


class WesternReturnService:
    """AstroSDK 2.0 service for planetary returns."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._crossing_service = AstronomyCrossingService(self.context, self._ephemeris)

    def find_planetary_return(
        self,
        planet: Planet,
        target_longitude: float,
        start_time: Time,
        max_days: float = 400.0,
    ) -> Time:
        """
        Finds the exact time when a planet returns to a target longitude.
        """
        return self._crossing_service.find_longitude_crossing(
            planet=planet,
            target_longitude=target_longitude,
            start_time=start_time,
            max_days=max_days
        )
