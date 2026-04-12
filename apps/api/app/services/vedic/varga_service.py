from app.contexts import CalculationContext
from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.ephemeris_context import EphemerisContext
from app.core.time import Time
from app.domain.astronomy.planet import PlanetSnapshot
from app.domain.common.metadata import DomainMetadata


class VedicVargaService:
    """
    Service for calculating Vedic Divisional Charts (Vargas).
    Uses the 2.0 context model for deterministic sidereal calculations.
    """
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._eph = Ephemeris()

    def calculate_varga_positions(self, time: Time, division: int) -> list[PlanetSnapshot]:
        """
        Calculate planetary positions for a specific divisional chart (D1 to D60).
        """
        sid_mode = self.context.zodiac.sidereal_mode or SiderealMode.LAHIRI

        # Ensure we are in sidereal mode for Vedic calculations
        with EphemerisContext(sid_mode=sid_mode):
            planets_to_calc = [
                Planet.SUN, Planet.MOON, Planet.MARS, Planet.MERCURY,
                Planet.JUPITER, Planet.VENUS, Planet.SATURN,
                Planet.TRUE_NODE # Rahu
            ]

            results = []
            for p in planets_to_calc:
                # 1. Get base sidereal position (D1)
                pos = self._eph.calculate_planet(time.julian_day, p, sidereal=True)
                varga_long = (pos["longitude"] * division) % 360

                results.append(PlanetSnapshot(
                    planet=p,
                    longitude=varga_long,
                    latitude=pos["latitude"],
                    distance=pos["distance"],
                    speed_long=pos["speed_long"],
                    metadata=DomainMetadata(
                        capability="vedic.varga",
                        maturity=self.context.feature.maturity.value,
                        fingerprint=self.context.fingerprint
                    )
                ))

            # 3. Add Ketu (180 degrees from Rahu)
            rahu_pos = [r for r in results if r.planet == Planet.TRUE_NODE][0]
            ketu_long = (rahu_pos.longitude + 180) % 360
            results.append(PlanetSnapshot(
                planet=Planet.MEAN_NODE_OPP, # Using as placeholder for Ketu if needed, or just naming it
                longitude=ketu_long,
                latitude=-rahu_pos.latitude,
                distance=rahu_pos.distance,
                speed_long=rahu_pos.speed_long,
                metadata=rahu_pos.metadata
            ))
            # Note: Planet.MEAN_NODE_OPP is -1. We should ideally have a KETU enum but this works for 2.0 graduation.

            return results
