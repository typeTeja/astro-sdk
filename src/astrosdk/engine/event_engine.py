from typing import List
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet
from ..domain.event import AstroEvent
from ..services.event_service import EventService

class EventEngine:
    """
    High-level orchestration for scanning and providing events.
    """
    def __init__(self):
        self._ephemeris = Ephemeris()
        self._event_service = EventService(self._ephemeris)

    def scan_events(self, start_time: Time, end_time: Time, planets: List[Planet]) -> List[AstroEvent]:
        """
        Orchestrates various event scans into a single list.
        """
        events = []
        for p in planets:
            events.extend(self._event_service.scan_ingresses(p, start_time, end_time))
            events.extend(self._event_service.scan_stations(p, start_time, end_time))
        return events
