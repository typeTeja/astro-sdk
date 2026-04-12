from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.research.financial import TimeWindow


class ResearchFinancialService:
    """
    Native 2.0 service for research in financial time cycles.
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def get_time_windows(
        self,
        start_time: Time,
        end_time: Time,
        planets: list[Planet] | None = None
    ) -> list[TimeWindow]:
        """
        Calculates distinct bounded periods like retrogrades and shadow phases.
        """
        from app.services.mundane.station_service import MundaneStationService
        station_service = MundaneStationService(self.context, ephemeris=self._eph)

        windows: list[TimeWindow] = []

        if not planets:
            planets = [
                Planet.MERCURY, Planet.JUPITER, Planet.SATURN,
                Planet.URANUS, Planet.NEPTUNE, Planet.PLUTO,
            ]

        # Scan for retrogrades in the period
        for planet in planets:
            # Look backwards and forwards to catch active retrogrades
            scan_start = Time.from_julian_day(start_time.julian_day - 180)
            scan_end = Time.from_julian_day(end_time.julian_day + 180)

            stations = station_service.scan_stations(planet, scan_start, scan_end)

            # Map stations to contiguous windows
            for i in range(len(stations)):
                if stations[i].station_type == "RETROGRADE":
                    r_start = stations[i].time
                    r_end = None
                    # Find the next DIRECT station
                    for j in range(i + 1, len(stations)):
                        if stations[j].station_type == "DIRECT":
                            r_end = stations[j].time
                            break

                    if r_end:
                        # Check overlap with requested window
                        req_start = start_time.dt
                        req_end = end_time.dt
                        if (r_start <= req_end and r_end >= req_start):
                            windows.append(
                                TimeWindow(
                                    planet=planet,
                                    start_time=r_start,
                                    end_time=r_end,
                                    event_type="RETROGRADE_PHASE",
                                    metadata={
                                        "duration_days": (r_end - r_start).days,
                                        "fingerprint": self.context.fingerprint
                                    },
                                )
                            )

        # Sort chronologically by start date
        windows.sort(key=lambda w: w.start_time)
        return windows
