from ..core.constants import SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.planet import PlanetPosition
from ..domain.transit import TransitAspect
from .aspect_service import AspectService
from .natal_service import NatalService


class TransitService:
    """
    Service for calculating transit-to-natal interactions.
    Returns domain objects (TransitAspect). Schema conversion is the router's responsibility.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris
        self.aspect_service = AspectService()
        self.natal_service = NatalService(ephemeris)

    def calculate_transit_aspects(
        self,
        natal_positions: list["PlanetPositionInputData"],  # type: ignore[name-defined]
        transit_time: Time,
        sidereal_mode: SiderealMode | None = SiderealMode.LAHIRI,
        aspect_types: list[str] | None = None,
        global_orb: float | None = None,
        heliocentric: bool = False,
        is_sidereal: bool = True,
    ) -> list[TransitAspect]:
        """
        Compare current planetary positions (transits) against stored natal positions.
        Returns domain TransitAspect objects.
        """
        effective_sidereal = is_sidereal and sidereal_mode is not None

        # 1. Calculate current transit positions
        transit_objs: list[PlanetPosition] = self.natal_service.calculate_positions(
            transit_time,
            sidereal_mode=sidereal_mode,
            heliocentric=heliocentric,
            is_sidereal=effective_sidereal,
        )

        # 2. Build orb table
        orbs = self.aspect_service.DEFAULT_ORBS.copy()
        if global_orb is not None:
            for k in orbs:
                orbs[k] = global_orb
        allowed_aspects = {name.upper() for name in aspect_types} if aspect_types else None

        found_aspects: list[TransitAspect] = []

        # 3. Transit-to-natal scan
        for tp in transit_objs:
            for np in natal_positions:
                np_lon = float(np.longitude)  # type: ignore[attr-defined]
                np_planet_name: str = str(np.planet)  # type: ignore[attr-defined]

                diff = abs(tp.longitude - np_lon)
                if diff > 180:
                    diff = 360 - diff

                for angle, aspect_name in self.aspect_service.MAJOR_ASPECTS.items():
                    if allowed_aspects is not None and aspect_name.upper() not in allowed_aspects:
                        continue
                    orb = abs(diff - angle)
                    limit = orbs.get(aspect_name, 2.0)

                    if orb <= limit:
                        # Canonical applying/separating from SKILL.md §5.2
                        angular_diff = (tp.longitude - np_lon + 180) % 360 - 180
                        if angle == 0.0:
                            is_applying = (angular_diff > 0 and tp.speed_long < 0) or (
                                angular_diff < 0 and tp.speed_long > 0
                            )
                        elif angle == 180.0:
                            if angular_diff > 0:
                                is_applying = tp.speed_long < 0 and angular_diff < 180
                            else:
                                is_applying = tp.speed_long > 0 and angular_diff > -180
                        else:
                            is_applying = (
                                tp.speed_long < 0 if angular_diff > 0 else tp.speed_long > 0
                            )

                        found_aspects.append(
                            TransitAspect(
                                transit_planet=tp.planet,
                                natal_planet=np_planet_name,
                                aspect_type=aspect_name,
                                angle=diff,
                                orb=orb,
                                is_applying=is_applying,
                            )
                        )

        return found_aspects
