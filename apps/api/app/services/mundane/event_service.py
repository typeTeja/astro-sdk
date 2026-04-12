from typing import Any

from app.contexts import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.services.mundane.ingress_service import MundaneIngressService
from app.services.mundane.station_service import MundaneStationService


class MundaneEventService:
    """
    AstroSDK 2.0 Aggregation service for Mundane celestial events.
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()
        self._ingress_service = MundaneIngressService(context, ephemeris=self._eph)
        self._station_service = MundaneStationService(context, ephemeris=self._eph)

    def scan_multi_events(
        self,
        planets: list[Any],
        start: Time,
        end: Time,
        scan_ingresses: bool = True,
        scan_stations: bool = True,
        **kwargs: Any
    ) -> list[Any]:
        """
        Scan for both ingresses and stations in the given period.
        """
        results: list[Any] = []

        for p in planets:
            if scan_ingresses:
                results.extend(self._ingress_service.scan_ingresses(p, start, end))
            if scan_stations:
                results.extend(self._station_service.scan_stations(p, start, end))

        results.sort(key=lambda x: x.time if hasattr(x, "time") else x.julian_day)
        return results
