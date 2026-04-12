from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata
from app.domain.research.correlation import CycleCorrelation
from app.services.mundane.station_service import MundaneStationService


class ResearchCorrelationService:
    """
    Native 2.0 service for astronomical cycle correlation.
    Maps planetary events (retrogrades, ingresses) to temporal windows.
    """

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._station_service = MundaneStationService(context, ephemeris=self._ephemeris)

    def get_retrograde_windows(
        self,
        planets: list[Planet],
        start_time: Time,
        end_time: Time
    ) -> list[CycleCorrelation]:
        """
        Calculates distinct bounded periods for planetary retrogrades.
        """
        correlations: list[CycleCorrelation] = []

        # Scan for stations in the period (padded slightly to catch active windows)
        scan_start = Time.from_julian_day(start_time.julian_day - 120)
        scan_end = Time.from_julian_day(end_time.julian_day + 120)

        for planet in planets:
            # Uses 2.0 StationService for detection
            stations = self._station_service.scan_stations(planet, scan_start, scan_end)

            # Sort stations to pair them up
            stations.sort(key=lambda s: s.time)

            for i in range(len(stations)):
                if stations[i].station_type == "RETROGRADE":
                    r_start = stations[i].time
                    r_end = None

                    # Look for the next DIRECT station
                    for j in range(i + 1, len(stations)):
                        if stations[j].station_type == "DIRECT":
                            r_end = stations[j].time
                            break

                    if r_end and r_start <= end_time.dt and r_end >= start_time.dt:
                        correlations.append(
                                CycleCorrelation(
                                    planet=planet,
                                    event_type="RETROGRADE",
                                    start_time=r_start,
                                    end_time=r_end,
                                    metadata=DomainMetadata(
                                        capability="research.correlation",
                                        maturity=self.context.feature.maturity.value,
                                        fingerprint=f"v2-retro-cycle-{planet.name}-{r_start.isoformat()}"
                                    ),
                                    properties={"duration_days": (r_end - r_start).days}
                                )
                            )

        correlations.sort(key=lambda c: c.start_time)
        return correlations
