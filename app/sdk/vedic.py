from ..contexts.calculation import CalculationContext
from ..services.vedic.panchanga_service import VedicPanchangaService
from ..core.ephemeris import Ephemeris
from ..core.time import Time


class VedicModule:
    """SDK interface for Vedic Astrology."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._service = VedicPanchangaService(context, ephemeris=Ephemeris())

    def get_panchang(self, time: Time, lat: float, lon: float):
        """Calculate the five elements of the Vedic calendar."""
        return self._service.calculate_panchanga(time, lat, lon)
