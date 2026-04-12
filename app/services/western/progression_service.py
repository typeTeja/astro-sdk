from app.contexts import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.western.progression import ProgressedChart
from app.services.astronomy.planetary_service import AstronomyPlanetaryService
from app.domain.common.metadata import DomainMetadata


class WesternProgressionService:
    """AstroSDK 2.0 service for Western progressions."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._planetary_service = AstronomyPlanetaryService(self.context, self._ephemeris)

    def calculate_secondary_progression(
        self,
        natal_time: Time,
        target_time: Time,
    ) -> ProgressedChart:
        """
        Calculates secondary progression using the day-for-a-year formula.
        """
        # (TargetTime - NatalTime) in days
        delta_days = target_time.julian_day - natal_time.julian_day
        
        # 1 day = 1 year (365.2425 days average tropical year)
        progression_delta = delta_days / 365.242199
        
        # Progressed Time
        prog_jd = natal_time.julian_day + progression_delta
        prog_time = Time.from_julian_day(prog_jd)
        
        # Calculate positions at progressed time
        planets = self._planetary_service.calculate_positions(prog_time)
        
        return ProgressedChart(
            natal_time=natal_time.dt,
            progressed_time=prog_time.dt,
            target_time=target_time.dt,
            planets=tuple(planets),
            metadata=DomainMetadata(
                capability="western.progression",
                maturity=self.context.feature.maturity.value,
                fingerprint=self.context.fingerprint
            )
        )
