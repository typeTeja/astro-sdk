from datetime import timedelta
from typing import Any

from ..core.constants import Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.financial import MarketCycleCorrelation, TimeWindow
from .events_service import EventsService


class FinancialTimeService:
    """
    High-precision event service for research in financial time cycles.
    Strictly provides astronomical data.
    """

    def __init__(self, ephemeris: Ephemeris, events_service: EventsService) -> None:
        self.eph = ephemeris
        self.events_service = events_service

    def get_time_windows(
        self, start_time: Time, end_time: Time, planets: list[Planet] | None = None
    ) -> list[TimeWindow]:
        """
        Calculates distinct bounded periods like retrogrades and shadow phases.
        """
        windows: list[TimeWindow] = []

        if not planets:
            # Default to slower market movers and Mercury for communications
            planets = [
                Planet.MERCURY,
                Planet.JUPITER,
                Planet.SATURN,
                Planet.URANUS,
                Planet.NEPTUNE,
                Planet.PLUTO,
            ]

        # Scan for retrogrades in the period
        for planet in planets:
            # Look backwards and forwards to catch active retrogrades
            scan_start = Time.from_julian_day(start_time.julian_day - 60)
            scan_end = Time.from_julian_day(end_time.julian_day + 60)
            
            # Use the events service to get station times
            stations = self.events_service.get_retrograde_stations(
                scan_start, planet, count=6
            )
            
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
                        if start_time.dt <= r_start <= end_time.dt or start_time.dt <= r_end <= end_time.dt or (r_start <= start_time.dt and r_end >= end_time.dt):
                            windows.append(
                                TimeWindow(
                                    planet=planet,
                                    start_time=r_start,
                                    end_time=r_end,
                                    event_type="RETROGRADE_PHASE",
                                    metadata={"duration_days": (r_end - r_start).days},
                                )
                            )

        # Sort chronologically by start date
        windows.sort(key=lambda w: w.start_time)
        return windows

    def get_market_cycles(self, start_time: Time, end_time: Time) -> list[MarketCycleCorrelation]:
        """
        Returns high-level cycle structures mapped (like composite major ingresses).
        """
        # We will stub this to use MarketCycleCorrelation domain object for now
        # until the composite scanner logic is fully built
        return []
