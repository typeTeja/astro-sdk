from ..contexts.calculation import CalculationContext
from ..services.western.chart_service import WesternChartService
from ..core.time import Time


class WesternModule:
    """SDK interface for Western Astrology."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._service = WesternChartService(context)

    def compute_natal(self, time: Time, lat: float, lon: float):
        """Generate a complete natal chart."""
        return self._service.create_chart(time, lat, lon)

    def compute_transits(self, time: Time, lat: float, lon: float):
        """Generate a transit chart for a specific moment."""
        return self._service.create_chart(time, lat, lon)
