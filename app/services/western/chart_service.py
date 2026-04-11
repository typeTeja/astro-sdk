from ...contexts import CalculationContext
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...domain.chart import Chart
from ...services.natal_service import NatalService


class WesternChartService:
    """Phase 0 adapter that runs chart generation through the 2.0 context model."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._natal_service = NatalService(self._ephemeris)

    def create_chart(self, time: Time, lat: float, lon: float) -> Chart:
        zodiac = self.context.zodiac
        coordinate = self.context.coordinate
        house = self.context.house

        planets = self._natal_service.calculate_positions(
            time=time,
            sidereal_mode=zodiac.sidereal_mode,
            heliocentric=coordinate.is_heliocentric,
            is_sidereal=zodiac.is_sidereal,
        )
        houses = self._natal_service.calculate_houses(
            time=time,
            lat=lat,
            lon=lon,
            system=house.system,
            sidereal_mode=zodiac.sidereal_mode,
            is_sidereal=zodiac.is_sidereal,
        )

        sidereal_name = (
            zodiac.sidereal_mode.name if zodiac.sidereal_mode is not None else "TROPICAL"
        )

        return Chart(
            metadata={
                "capability": self.context.feature.capability,
                "maturity": self.context.feature.maturity.value,
                "zodiac": zodiac.zodiac.value,
                "sidereal_mode": sidereal_name,
                "coordinate_system": coordinate.system.value,
                "house_system": house.system.name,
                "lat": str(lat),
                "lon": str(lon),
            },
            time=time,
            planets=planets,
            houses=houses,
        )
