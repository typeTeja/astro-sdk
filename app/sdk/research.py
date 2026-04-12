from collections.abc import Generator
from datetime import timedelta
from typing import Any

from ..contexts.calculation import CalculationContext
from ..core.time import Time
from ..services.research.export_service import ResearchExportService
class ResearchModule:
    """SDK interface for Research and bulk data operations."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._export_service = ResearchExportService(context)

    def generate_series(
        self, planets: list[Any], start: Time, end: Time, step: timedelta
    ) -> Generator[Any, None, None]:
        """Streaming generator for planetary positions."""
        return self._export_service.stream_ephemeris(planets, start, end, step)
