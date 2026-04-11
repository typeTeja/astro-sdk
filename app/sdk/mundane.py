from ..contexts.calculation import CalculationContext
from ..services.mundane.event_service import EventService
from ..core.time import Time


class MundaneModule:
    """SDK interface for Mundane Astrology and event scanning."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._service = EventService(context)

    def scan_events(self, planets: list, start: Time, end: Time, **kwargs):
        """Scans for celestial events (Ingresses, Stations, etc.) using the 2.0 Engine."""
        return self._service.scan_multi_events(planets, start, end, **kwargs)
