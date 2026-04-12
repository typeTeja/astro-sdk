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
        observer = self.context.observer

        # Manage Topocentric state if required
        is_topo = coordinate.is_topocentric
        if is_topo:
            # Note: observer is guaranteed to be non-None by API validation if is_topocentric
            assert observer is not None
            self._eph.set_topocentric(observer.latitude, observer.longitude, observer.altitude)

        results = []
        try:
            for p_enum in target_planets:
                pos = self._eph.calculate_planet(
                    time.julian_day,
                    p_enum,
                    sidereal=zodiac.is_sidereal,
                    heliocentric=coordinate.is_heliocentric,
                    topocentric=is_topo
                )

                results.append(
                    PlanetSnapshot(
                        planet=p_enum,
                        longitude=pos["longitude"],
                        latitude=pos["latitude"],
                        distance=pos["distance"],
                        speed_long=pos["speed_long"],
                        metadata=DomainMetadata(
                            capability="astronomy.planet",
                            maturity=self.context.feature.maturity.value,
                            fingerprint=self.context.fingerprint
                        )
                    )
                )
        finally:
            # Reset topocentric state to Geocentric to maintain singleton purity
            if is_topo:
                self._eph.reset_topocentric()

        return results
