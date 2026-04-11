from ...contexts import CalculationContext
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...domain.transit import ProgressedChart
from ...services.progression_service import ProgressionService


class WesternProgressionService:
    """Phase 1 adapter for progression calculation via the 2.0 context model."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._progression_service = ProgressionService(self._ephemeris)

    def calculate_secondary_progression(
        self,
        natal_time: Time,
        target_time: Time,
    ) -> ProgressedChart:
        zodiac = self.context.zodiac
        sidereal_mode = zodiac.sidereal_mode

        if not zodiac.is_sidereal:
            sidereal_mode = None

        return self._progression_service.calculate_secondary_progression(
            natal_time,
            target_time,
            sidereal_mode=sidereal_mode,
            is_sidereal=zodiac.is_sidereal,
        )
