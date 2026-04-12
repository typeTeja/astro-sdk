from typing import Any

from app.contexts import CalculationContext
from app.core.constants import HouseSystem, Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata


class AstronomySectorService:
    """
    Native 2.0 service for calculating planetary sector distributions (Gauquelin, 36-Sectors).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def get_sectors(
        self,
        time: Time,
        lat: float,
        lon: float,
        num_sectors: int = 36
    ) -> list[dict[str, Any]]:
        """
        Calculate the sector position for all major planets using the diurnal cycle.
        """
        from app.core.ephemeris_context import EphemerisContext

        # Geocentric scanning
        with EphemerisContext(topo=None):
            axes = self._eph.calculate_houses(time.julian_day, lat, lon, HouseSystem.PLACIDUS)
            asc = axes["ascendant"]

            results = []
            planets_to_scan = [
                Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS,
                Planet.MARS, Planet.JUPITER, Planet.SATURN, Planet.URANUS,
                Planet.NEPTUNE, Planet.PLUTO,
            ]

            for p in planets_to_scan:
                p_pos = self._eph.calculate_planet(time.julian_day, p, sidereal=False)
                dist_asc = (asc - p_pos["longitude"]) % 360
                sector_num = int(dist_asc / (360.0 / num_sectors)) + 1

                results.append({
                    "planet": p.name,
                    "sector": sector_num,
                    "intensity": 1.0, # Simple occupancy
                    "metadata": DomainMetadata(
                        capability="astronomy.sector",
                        maturity=self.context.feature.maturity.value,
                        fingerprint=self.context.fingerprint
                    )
                })

            return results
