from ..core.constants import SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.planet import PlanetPosition
from ..domain.transit import ProgressedChart
from .natal_service import NatalService


class ProgressionService:
    """
    Service for calculating planetary progressions (Secondary, Solar Arc, etc.).
    Returns domain objects. Schema conversion is the router's responsibility.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris
        self.natal_service = NatalService(ephemeris)

    def calculate_secondary_progression(
        self,
        natal_time: Time,
        target_time: Time,
        sidereal_mode: SiderealMode | None = SiderealMode.LAHIRI,
        is_sidereal: bool = True,
    ) -> ProgressedChart:
        """
        Calculate secondary progression (1 day = 1 year).
        Returns a ProgressedChart domain object.
        """
        # 1. Calculate the progression JD (1 tropical year = 365.242189 days)
        diff_days = target_time.julian_day - natal_time.julian_day
        prog_jd = natal_time.julian_day + (diff_days / 365.242189)
        prog_time = Time.from_julian_day(prog_jd)

        # 2. Get positions for that JD
        positions: list[PlanetPosition] = self.natal_service.calculate_positions(
            prog_time,
            sidereal_mode=sidereal_mode,
            is_sidereal=is_sidereal,
        )

        # 3. Build plain-dict records (no schema coupling)
        planets_data: list[dict[str, object]] = [
            {
                "planet": p.planet.name,
                "longitude": p.longitude,
                "latitude": p.latitude,
                "distance": p.distance,
                "speed_long": p.speed_long,
                "is_retrograde": p.is_retrograde,
                "sign": int(p.sign) + 1,
                "sign_name": p.sign_name,
            }
            for p in positions
        ]

        return ProgressedChart(
            progression_date=prog_time.dt,
            planets=planets_data,
        )
