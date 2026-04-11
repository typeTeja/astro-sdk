from types import SimpleNamespace

from ...contexts import CalculationContext
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...domain.planet import PlanetPosition
from ...domain.transit import TransitAspect
from ...services.transit_service import TransitService


class WesternTransitService:
    """Phase 0 adapter for transit-to-natal scanning via the 2.0 context model."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()
        self._transit_service = TransitService(self._ephemeris)

    def scan_transits(
        self,
        natal_positions: list[PlanetPosition],
        transit_time: Time,
        aspect_types: list[str] | None = None,
        global_orb: float | None = None,
    ) -> list[TransitAspect]:
        zodiac = self.context.zodiac
        coordinate = self.context.coordinate

        natal_inputs = [
            SimpleNamespace(longitude=position.longitude, planet=position.planet.name)
            for position in natal_positions
        ]

        return self._transit_service.calculate_transit_aspects(
            natal_inputs,
            transit_time,
            sidereal_mode=zodiac.sidereal_mode,
            aspect_types=aspect_types,
            global_orb=global_orb,
            heliocentric=coordinate.is_heliocentric,
            is_sidereal=zodiac.is_sidereal,
        )
