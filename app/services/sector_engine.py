from ..core.constants import HouseSystem, Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..schemas.vedic import SectorHitSchema


class SectorEngine:
    """
    Engine for calculating planetary sector distributions (Gauquelin, 36-Sectors).
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris

    def calculate_sectors(
        self, time: Time, lat: float, lon: float, num_sectors: int = 36
    ) -> list[SectorHitSchema]:
        """
        Calculate the sector position for all major planets using the diurnal cycle.
        Sectors start from the Ascendant (1) and move clockwise toward the MC.
        Gauquelin sectors usually count 1-12 or 1-36.
        """
        # 1. Get House Axes for boundaries
        axes = self.eph.calculate_houses(time.julian_day, lat, lon, HouseSystem.PLACIDUS)
        asc = axes["ascendant"]

        sector_results = []

        # Allowed planets for sector research
        planets_to_scan = [
            Planet.SUN,
            Planet.MOON,
            Planet.MERCURY,
            Planet.VENUS,
            Planet.MARS,
            Planet.JUPITER,
            Planet.SATURN,
            Planet.URANUS,
            Planet.NEPTUNE,
            Planet.PLUTO,
        ]

        for p_id in planets_to_scan:
            p_pos = self.eph.calculate_planet(time.julian_day, p_id, sidereal=False)
            p_lon = p_pos["longitude"]

            # Distance from Ascendant (clockwise)
            dist_asc = (asc - p_lon) % 360

            # 1 to num_sectors
            sector_num = int(dist_asc / (360.0 / num_sectors)) + 1

            sector_results.append(
                SectorHitSchema(
                    planet=str(p_id.name),
                    sector=sector_num,
                    intensity=1.0,  # Placeholder for exact peak proximity
                )
            )

        return sector_results
