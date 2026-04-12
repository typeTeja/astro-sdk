from app.contexts import CalculationContext
from app.core.constants import Planet
from app.domain.western.aspect import Aspect
from app.domain.astronomy.planet import PlanetSnapshot


class WesternAspectService:
    """Native 2.0 service for Western aspect calculations."""

    def __init__(self, context: CalculationContext) -> None:
        self.context = context

    def calculate_aspects(
        self,
        planets: list[PlanetSnapshot],
        aspect_types: list[str] | None = None,
        global_orb: float | None = None,
    ) -> list[Aspect]:
        """
        Calculates stationary aspects between a list of planet positions.
        """
        results = []
        
        # Default aspect set if none provided
        target_aspects = aspect_types or ["Conjunction", "Opposition", "Trine", "Square", "Sextile"]
        max_orb = global_orb if global_orb is not None else 8.0
        
        # Basic aspect angles
        ASPECT_DEGREES = {
            "Conjunction": 0,
            "Opposition": 180,
            "Trine": 120,
            "Square": 90,
            "Sextile": 60,
        }

        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                p1, p2 = planets[i], planets[j]
                
                # Use only requested aspects found in our mapping
                for aspect_name in target_aspects:
                    if aspect_name not in ASPECT_DEGREES:
                        continue
                        
                    target_angle = ASPECT_DEGREES[aspect_name]
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
                                applying=True # Simple snapshot assumes applying for legacy compatibility
                            )
                        )
        return results
