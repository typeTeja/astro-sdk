from app.contexts import CalculationContext
from app.domain.astronomy.planet import PlanetSnapshot
from app.domain.western.aspect import Aspect


class WesternAspectService:
    """Native 2.0 service for Western aspect calculations."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context

    def calculate_aspects(
        self,
        planets: list[PlanetSnapshot],
        points_b: list[PlanetSnapshot] | None = None,
        aspect_types: list[str] | None = None,
        global_orb: float | None = None,
    ) -> list[Aspect]:
        """
        Detect geometric aspects between planets.
        If points_b is provided, calculates aspects between planets and points_b (Synastry/Transits).
        Otherwise, calculates all internal aspects within the planets list.
        """
        results = []
        max_orb = global_orb if global_orb is not None else 8.0

        # Basic aspect angles
        aspect_degrees = {
            "Conjunction": 0,
            "Opposition": 180,
            "Trine": 120,
            "Square": 90,
            "Sextile": 60,
        }
        target_aspects = aspect_types or list(aspect_degrees.keys())

        # Decide comparison lists
        list_a = planets
        list_b = points_b if points_b is not None else planets

        for i, p1 in enumerate(list_a):
            # If internal comparison, avoid double counting and self-aspects
            start_idx = i + 1 if points_b is None else 0
            for p2 in list_b[start_idx:]:
                if p1.planet == p2.planet and points_b is None:
                    continue

                # Use only requested aspects found in our mapping
                for aspect_name in target_aspects:
                    if aspect_name not in aspect_degrees:
                        continue

                    target_angle = aspect_degrees[aspect_name]
                    diff = abs(p1.longitude - p2.longitude) % 360
                    if diff > 180:
                        diff = 360 - diff

                    orb = abs(diff - target_angle)

                    if orb <= max_orb:
                        results.append(
                            Aspect(
                                p1=p1.planet,
                                p2=p2.planet,
                                angle=diff,
                                orb=orb,
                                type=aspect_name,
                                applying=True
                            )
                        )
        return results
