from app.contexts import CalculationContext
from app.core.constants import ALLOWED_PLANETS, Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata
from app.domain.mundane.station import StationEvent


class MundaneStationService:
    """
    Service for detecting planetary station events (Retrograde/Direct).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def scan_stations(self, planet: Planet, start_time: Time, end_time: Time) -> list[StationEvent]:
        """
        Scans for all turning points of a planet between two dates.
        """
        if planet not in ALLOWED_PLANETS or planet in [Planet.SUN, Planet.MOON]:
            return []

        events: list[StationEvent] = []
        current_jd = start_time.julian_day
        end_jd = end_time.julian_day

        # Advance through time searching for speed sign flips
        while current_jd < end_jd:
            station_jd = self._eph.calculate_stationary_point(current_jd, planet, forward=True, max_days=30.0)

            if station_jd and station_jd < end_jd:
                # Determine type by checking speed after station
                pos_after = self._eph.calculate_planet(station_jd + 0.1, planet)
                station_type = "RETROGRADE" if pos_after["speed_long"] < 0 else "DIRECT"

                events.append(
                    StationEvent(
                        planet=planet,
                        station_type=station_type,
                        time=Time.from_julian_day(station_jd).dt,
                        metadata=DomainMetadata(
                            capability="mundane.stations",
                            maturity=self.context.feature.maturity.value,
                            fingerprint=self.context.fingerprint
                        )
                    )
                )
                current_jd = station_jd + 1.0 # Buffer escape
            else:
                current_jd += 30.0 # Wide skip

        return events
