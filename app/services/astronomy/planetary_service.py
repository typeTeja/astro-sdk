from app.contexts import CalculationContext
from app.core.constants import ALLOWED_PLANETS, Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.astronomy.planet import PlanetSnapshot
from app.domain.common.metadata import DomainMetadata


class AstronomyPlanetaryService:
    """AstroSDK 2.0 service for raw planetary calculations."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def calculate_positions(
        self,
        time: Time,
        planets: list[Planet] | None = None,
    ) -> list[PlanetSnapshot]:
        """Calculates positions for a list of planets using the current context."""
        target_planets = planets or list(ALLOWED_PLANETS)
        
        zodiac = self.context.zodiac
        coordinate = self.context.coordinate
        
        results = []
        for p_enum in target_planets:
            pos = self._eph.calculate_planet(
                time.julian_day,
                p_enum,
                sidereal=zodiac.is_sidereal,
                heliocentric=coordinate.is_heliocentric
            )
            
            results.append(
                PlanetSnapshot(
                    planet=p_enum,
                    longitude=pos["longitude"],
                    latitude=pos["latitude"],
                    distance=pos["distance"],
                    metadata=DomainMetadata(
                        capability="astronomy.planet",
                        maturity=self.context.feature.maturity.value,
                        fingerprint=self.context.fingerprint
                    )
                )
            )
        return results
