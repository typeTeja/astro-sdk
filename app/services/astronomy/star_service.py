from app.contexts import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.ephemeris_context import EphemerisContext
from app.core.time import Time
from app.domain.astronomy.fixed_star import FixedStarPosition
from app.domain.common.metadata import DomainMetadata


class AstronomyStarService:
    """
    Native 2.0 service for calculating fixed star positions.
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def get_star_position(
        self, 
        star_name: str, 
        time: Time
    ) -> FixedStarPosition:
        """
        Calculate position for a single star using current context.
        """
        is_sidereal = self.context.zodiac.zodiac == "sidereal" or self.context.zodiac.sidereal_mode is not None
        sid_mode = self.context.zodiac.sidereal_mode
        
        with EphemerisContext(sid_mode=sid_mode):
            data = self._eph.calculate_fixed_star(time.julian_day, star_name, sidereal=is_sidereal)
            
            return FixedStarPosition(
                name=data["name"],
                longitude=data["longitude"],
                latitude=data["latitude"],
                magnitude=data["magnitude"],
                metadata=DomainMetadata(
                    capability="astronomy.star",
                    maturity=self.context.feature.maturity.value,
                    fingerprint=self.context.fingerprint
                )
            )

    def get_stars_positions(
        self, 
        star_names: list[str], 
        time: Time
    ) -> list[FixedStarPosition]:
        """
        Calculate positions for multiple stars.
        """
        return [self.get_star_position(name, time) for name in star_names]
