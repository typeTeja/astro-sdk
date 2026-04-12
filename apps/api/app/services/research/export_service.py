from collections.abc import Generator
from datetime import timedelta

from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time


class ResearchExportService:
    """Service for bulk exporting astronomical data for research."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def stream_ephemeris(
        self,
        planets: list[Planet],
        start_time: Time,
        end_time: Time,
        step: timedelta,
        format: str = "CSV"
    ) -> Generator[str, None, None]:
        """
        Stream planetary positions as a formatted string (CSV).
        """
        if format.upper() == "CSV":
            header = "time,planet,longitude,latitude,distance,speed_long\n"
            yield header

        curr_jd = start_time.julian_day
        end_jd = end_time.julian_day
        step_jd = step.total_seconds() / 86400.0

        while curr_jd <= end_jd:
            t = Time.from_julian_day(curr_jd)
            for p in planets:
                pos = self._eph.calculate_planet(
                    curr_jd,
                    p,
                    sidereal=self.context.zodiac.is_sidereal,
                    heliocentric=self.context.coordinate.is_heliocentric
                )
                row = f"{t.dt.isoformat()},{p.name},{pos['longitude']:.6f},{pos['latitude']:.6f},{pos['distance']:.8f},{pos['speed_long']:.6f}\n"
                yield row
            curr_jd += step_jd
