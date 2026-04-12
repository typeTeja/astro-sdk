from app.core.clock import get_current_time
import logging
from datetime import datetime
from typing import Any

from dateutil.parser import parse as parse_date  # type: ignore

from ..contexts.factories import create_default_context
from ..core.time import Time
from ..services.mundane.event_service import MundaneEventService

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
        service = MundaneEventService(context, ephemeris=self._ephemeris)

        # 2. Extract params
        planets = params.get("planets", [])

        start_val = params.get("start_time")
        end_val = params.get("end_time")

        start_dt = parse_date(start_val) if isinstance(start_val, str) else start_val
        end_dt = parse_date(end_val) if isinstance(end_val, str) else end_val

        if not isinstance(start_dt, datetime) or not isinstance(end_dt, datetime):
             raise ValueError("start_time and end_time must be datetime objects or ISO strings")

        start_time = Time(start_dt)
        end_time = Time(end_dt)
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
            "timestamp": get_current_time().isoformat()
        }
