from ...contexts import CalculationContext
from ...domain.aspect import Aspect
from ...domain.planet import PlanetPosition
from ...services.aspect_service import AspectService


class WesternAspectService:
    """Phase 0 adapter for direct aspect calculation via the 2.0 context model."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._aspect_service = AspectService()

    def calculate_aspects(
        self,
        planets: list[PlanetPosition],
        aspect_types: list[str] | None = None,
        global_orb: float | None = None,
    ) -> list[Aspect]:
        return self._aspect_service.calculate_aspects(
            planets,
            aspect_types=aspect_types,
            global_orb=global_orb,
        )
