from ...contexts import CalculationContext
from ...core.constants import Planet
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...services.crossing_service import CrossingService


class WesternReturnService:
    """Phase 1 adapter for planetary returns via the 2.0 context model."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._crossing_service = CrossingService(self._ephemeris)

    def find_planetary_return(
        self,
        planet: Planet,
        target_longitude: float,
        start_time: Time,
        max_days: float = 400.0,
    ) -> Time:
        zodiac = self.context.zodiac
        coordinate = self.context.coordinate

        sidereal_mode = zodiac.sidereal_mode
        if not zodiac.is_sidereal:
            sidereal_mode = None

        return self._crossing_service.find_planetary_return(
            planet,
            target_longitude,
            start_time,
            sidereal_mode=sidereal_mode,
            heliocentric=coordinate.is_heliocentric,
            max_search_years=max_days / 365.25,
        )
