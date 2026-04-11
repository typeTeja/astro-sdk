from ..contexts.calculation import CalculationContext
from ..services.research.export_service import ExportService
from ..services.research.statistics_service import StatisticsService
from ..core.time import Time
from datetime import timedelta


class ResearchModule:
    """SDK interface for Research and bulk data operations."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._export_service = ExportService(context)
        self._stats_service = StatisticsService(context)

    def generate_series(self, planets: list, start: Time, end: Time, step: timedelta):
        """Streaming generator for planetary positions."""
        return self._export_service.stream_ephemeris(planets, start, end, step)

    def analyze_frequency(self, planet: list, start: Time, end: Time):
        """Frequency analysis for planetary states."""
        return self._stats_service.calculate_frequency(planet, start, end)
