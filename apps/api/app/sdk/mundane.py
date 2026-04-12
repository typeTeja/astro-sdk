from typing import Any

from ..contexts.calculation import CalculationContext
from ..core.time import Time
from ..services.mundane.event_service import MundaneEventService


class MundaneModule:
    """SDK interface for Mundane Astrology and event scanning."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._service = MundaneEventService(context)

    def scan_events(self, planets: list[Any], start: Time, end: Time, **kwargs: Any) -> list[Any]:
        """Scans for celestial events (Ingresses, Stations, etc.) using the 2.0 Engine."""
        return self._service.scan_multi_events(planets, start, end, **kwargs)
