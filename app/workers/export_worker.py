from app.core.clock import get_current_time
import logging
from datetime import datetime, timedelta
from typing import Any

from ..contexts.factories import create_default_context
from ..core.time import Time
from ..services.research.export_service import ResearchExportService

logger = logging.getLogger(__name__)

class ExportWorker:
    """
    Executes high-density data export jobs in the background.
    """
    def __init__(self, ephemeris: Any = None):
        self._ephemeris = ephemeris

    def run(self, job_id: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Main execution entry point for the worker.
        """
        logger.info(f"Starting ExportWorker for job {job_id}")

        # 1. Reconstruct context and service
        context = create_default_context() # Normally parsed from params
        service = ResearchExportService(context, ephemeris=self._ephemeris)

        # 2. Extract params
        start_raw = params.get("start_time")
        end_raw = params.get("end_time")

        from dateutil.parser import parse  # type: ignore
        start_dt = parse(start_raw) if isinstance(start_raw, str) else get_current_time()
        end_dt = parse(end_raw) if isinstance(end_raw, str) else start_dt + timedelta(days=30)

        planets = params.get("planets", [])
        start_time = Time(start_dt)
        end_time = Time(end_dt)
        step_days = params.get("step_days", 1)
        fmt = params.get("format", "CSV")

        # 3. Execute
        # For workers, we usually want to write to a file/buffer instead of streaming
        # but here we generate the full output for the Job result
        output = b"".join([
            chunk.encode() if isinstance(chunk, str) else chunk
            for chunk in service.stream_ephemeris(
                planets,
                start_time,
                end_time,
                step=timedelta(days=step_days),
                format=fmt
            )
        ])

        logger.info(f"ExportWorker completed job {job_id}")

        return {
            "status": "COMPLETED",
            "byte_count": len(output),
            "format": fmt,
            "timestamp": get_current_time().isoformat()
        }
