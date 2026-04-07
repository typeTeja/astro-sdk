from ..core.constants import SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..schemas.astro import PlanetPositionData
from ..schemas.transits import SecondaryProgressionData
from .natal_service import NatalService


class ProgressionService:
    """
    Service for calculating planetary progressions (Secondary, Solar Arc, etc.).
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris
        self.natal_service = NatalService(ephemeris)

    def calculate_secondary_progression(
        self,
        natal_time: Time,
        target_time: Time,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
    ) -> SecondaryProgressionData:
        """
        Calculate secondary progression (1 day = 1 year).
        """
        # 1. Calculate the 'Progression Day'
        # Difference in days
        diff_days = target_time.julian_day - natal_time.julian_day

        # 1 day of progression = 1 tropical year (~365.242189 days)
        prog_jd = natal_time.julian_day + (diff_days / 365.242189)
        prog_time = Time.from_julian_day(prog_jd)

        # 2. Get positions for that JD (returns list[PlanetPosition])
        positions = self.natal_service.calculate_positions(prog_time, sidereal_mode)

        # 3. Map to Schema (PlanetPositionData)
        planets_data = [
            PlanetPositionData(
                planet=p.planet.name,
                longitude=p.longitude,
                latitude=p.latitude,
                distance=p.distance,
                speed_long=p.speed_long,
                is_retrograde=p.is_retrograde,
                sign=p.sign,
                sign_name=p.sign_name,
            )
            for p in positions
        ]

        return SecondaryProgressionData(
            progression_date=prog_time.dt,
            planets=planets_data,
        )
