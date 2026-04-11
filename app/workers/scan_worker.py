import logging
from datetime import datetime
from typing import Any
from ..services.mundane.event_service import EventService
from ..core.time import Time
from ..contexts.factories import create_default_context

logger = logging.getLogger(__name__)

class ScanWorker:
    """
    Executes large-scale mundane event scanning in the background.
    """
    def __init__(self, ephemeris: Any = None):
        self._ephemeris = ephemeris

    def run(self, job_id: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Main execution entry point for the worker.
        """
        logger.info(f"Starting ScanWorker for job {job_id}")
        
        # 1. Reconstruct context and service
        context = create_default_context()
        service = EventService(context, ephemeris=self._ephemeris)
        
        # 2. Extract params
        planets = params.get("planets", [])
        start_time = Time(params.get("start_time"))
        end_time = Time(params.get("end_time"))
        scan_ingresses = params.get("scan_ingresses", True)
        scan_stations = params.get("scan_stations", True)
        
        # 3. Execute
        events = service.scan_multi_events(
            planets,
            start_time,
            end_time,
            scan_ingresses=scan_ingresses,
            scan_stations=scan_stations
        )
        
        logger.info(f"ScanWorker completed job {job_id} with {len(events)} hits")
        
        return {
            "status": "COMPLETED",
            "event_count": len(events),
            "events_summary": [f"{e.type} - {e.planet.name}" for e in events[:10]],
            "timestamp": datetime.now().isoformat()
        }
