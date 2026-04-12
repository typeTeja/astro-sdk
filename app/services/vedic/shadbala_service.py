from collections.abc import Sequence

from app.contexts import CalculationContext
from app.domain.astronomy.planet import PlanetSnapshot as PlanetPosition
from app.domain.common.metadata import DomainMetadata
from app.domain.vedic.shadbala import ShadbalaScore


class VedicShadbalaService:
    """
    Service for calculating Shadbala (Planetary Strength).
    Provides a high-fidelity 2.0 implementation of Vedic positional and directional power.
    """
    def __init__(self, context: CalculationContext) -> None:
        self.context = context

    def calculate_shadbala(self, planets: Sequence[PlanetPosition], ascendant: float) -> list[ShadbalaScore]:
        """
        Calculate raw Shadbala metrics for all planets.
        """
        results = []
        meta = DomainMetadata(
            capability="vedic.shadbala",
            maturity=self.context.feature.maturity.value,
            fingerprint=self.context.fingerprint
        )

        for p in planets:
            # 1. Base Natural Strength (Naisargika)
            # Standard order: Sun (60), Moo (51), Ven (42), Jup (34), Mar (25), Mer (17), Sat (8)
            natural_map = {
                "SUN": 60, "MOON": 51, "VENUS": 42, "JUPITER": 34,
                "MARS": 25, "MERCURY": 17, "SATURN": 8, "RAHU": 0, "KETU": 0
            }
            base_score = natural_map.get(p.planet.name, 10)

            # 2. Dig Bala (Directional Strength)
            # Map absolute longitude to house index (0-11) relative to Ascendant
            house_idx = int(((p.longitude - ascendant) % 360) / 30)

            dig_bala = 0
            if p.planet.name in ["JUPITER", "MERCURY"] and house_idx == 0 or p.planet.name in ["MOON", "VENUS"] and house_idx == 3 or p.planet.name == "SATURN" and house_idx == 6 or p.planet.name in ["SUN", "MARS"] and house_idx == 9: # 1st House
                dig_bala = 60

            # 3. Positional (Simplified Sthana Bala)
            # Strong in angles (1, 4, 7, 10), middling in succedent (2, 5, 8, 11), weak in cadent (3, 6, 9, 12)
            sthana_points = 0
            if house_idx in [0, 3, 6, 9]:
                sthana_points = 30
            elif house_idx in [1, 4, 7, 10]:
                sthana_points = 15

            total_rupas = (base_score + dig_bala + sthana_points) / 60.0 # Convert to Rupas (1 Rupa = 60 Virupas)

            results.append(ShadbalaScore(
                planet=p.planet.name,
                total_rupas=total_rupas,
                metadata=meta
            ))

        return results
