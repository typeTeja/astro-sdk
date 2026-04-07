from ..core.constants import SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..schemas.astro import PlanetPositionData
from ..schemas.transits import TransitAspectSchema
from .aspect_service import AspectService
from .natal_service import NatalService


class TransitService:
    """
    Service for calculating transit-to-natal interactions.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris
        self.aspect_service = AspectService()
        self.natal_service = NatalService(ephemeris)

    def calculate_transit_aspects(
        self,
        natal_positions: list[PlanetPositionData],
        transit_time: Time,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
        aspect_types: list[str] | None = None,
        global_orb: float | None = None,
    ) -> list[TransitAspectSchema]:
        """
        Compare current planetary positions (transits) against stored natal positions.
        """
        # 1. Calculate current transit positions
        transit_objs = self.natal_service.calculate_positions(transit_time, sidereal_mode)

        # 2. Aspect Scan
        found_aspects: list[TransitAspectSchema] = []

        # Orbs are usually tighter for transits, but we'll use defaults from aspect_service
        # unless overridden by global_orb
        orbs = self.aspect_service.DEFAULT_ORBS.copy()
        if global_orb is not None:
            for k in orbs:
                orbs[k] = global_orb

        # Manually iterate for T-to-N logic
        for tp in transit_objs:
            for np in natal_positions:
                diff = abs(tp.longitude - np.longitude)
                if diff > 180:
                    diff = 360 - diff

                # Check major aspects
                for angle, aspect_name in self.aspect_service.MAJOR_ASPECTS.items():
                    orb = abs(diff - angle)
                    limit = orbs.get(aspect_name, 2.0)

                    if orb <= limit:
                        found_aspects.append(
                            TransitAspectSchema(
                                transit_planet=tp.planet.name,
                                natal_planet=np.planet,  # natal_planet expected as str
                                aspect_type=aspect_name,
                                angle=diff,
                                orb=orb,
                                is_applying=False,  # Requires speed comparison
                            )
                        )

        return found_aspects
