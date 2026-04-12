from collections.abc import Sequence

from app.contexts import CalculationContext
from app.core.constants import ALLOWED_PLANETS
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.astronomy.planet import PlanetSnapshot
from app.domain.common.metadata import DomainMetadata
from app.domain.western.transit import TransitAspect


class WesternTransitService:
    """Native 2.0 service for transit-to-natal scanning."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()

    def scan_transits(
        self,
        natal_positions: Sequence[PlanetSnapshot],
        transit_time: Time,
        aspect_types: list[str] | None = None,
        global_orb: float | None = None,
    ) -> list[TransitAspect]:
        """
        Calculates aspects between transiting planets and fixed natal positions.
        """
        results = []

        # Calculate current transiting positions
        transit_planets = []
        for p_enum in ALLOWED_PLANETS:
            pos = self._ephemeris.calculate_planet(
                transit_time.julian_day,
                p_enum,
                sidereal=self.context.zodiac.is_sidereal,
                heliocentric=self.context.coordinate.is_heliocentric
            )
            transit_planets.append(
                PlanetSnapshot(
                    planet=p_enum,
                    longitude=pos["longitude"],
                    latitude=pos["latitude"],
                    distance=pos["distance"],
                    speed_long=pos["speed_long"],
                    metadata=DomainMetadata(capability="astronomy.planet", maturity="PROD", fingerprint="transit-scan")
                )
            )

        # Aspect definitions
        target_aspects = aspect_types or ["Conjunction", "Opposition", "Trine", "Square", "Sextile"]
        max_orb = global_orb if global_orb is not None else 8.0

        aspect_degrees = {
            "Conjunction": 0,
            "Opposition": 180,
            "Trine": 120,
            "Square": 90,
            "Sextile": 60,
        }

        for tp in transit_planets:
            for np in natal_positions:
                for aspect_name, target_angle in aspect_degrees.items():
                    if aspect_name not in target_aspects:
                        continue

                    diff = abs(tp.longitude - np.longitude) % 360
                    if diff > 180:
                        diff = 360 - diff

                    orb = abs(diff - target_angle)

                    if orb <= max_orb:
                        results.append(
                            TransitAspect(
                                transit_planet=tp.planet,
                                natal_planet=np.planet.name,
                                aspect_type=aspect_name,
                                angle=diff,
                                orb=orb,
                                is_applying=True,
                                metadata=DomainMetadata(
                                    capability="western.transit",
                                    maturity=self.context.feature.maturity.value,
                                    fingerprint=self.context.fingerprint
                                )
                            )
                        )
        return results
