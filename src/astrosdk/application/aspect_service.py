from typing import List, Optional
from astrosdk.domain.models.planet import PlanetPosition
from astrosdk.domain.models.aspect import Aspect
from astrosdk.core.constants import Planet
from astrosdk.config.astro_config import AstroConfig

class AspectService:
    """
    Service for calculating aspects between planetary positions.
    Configurable via injected AstroConfig.
    """
    
    def __init__(self, config: AstroConfig):
        self.config = config
        
    def calculate_aspects(
        self, 
        planets: List[PlanetPosition], 
        types: Optional[List[str]] = None
    ) -> List[Aspect]:
        
        # Logic is mostly pure math, similar to the old service.
        # But we use config for orbs.
        
        results = []
        orbs = self.config.aspect_orbs
        
        # Mapping aspect names to angles should ideally be in config or constants
        # Hardcoding standard ones for phase 1 refactor simplicity, 
        # but configured orbs are used.
        ASPECT_ANGLES = {
            "CONJUNCTION": 0.0,
            "SEXTILE": 60.0,
            "SQUARE": 90.0,
            "TRINE": 120.0,
            "OPPOSITION": 180.0
            # Add others as needed...
        }
        
        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                aspect = self._get_aspect(p1, p2, ASPECT_ANGLES, orbs)
                if aspect:
                    results.append(aspect)
        return results

    def _get_aspect(self, p1: PlanetPosition, p2: PlanetPosition, angles: dict, orbs: dict) -> Optional[Aspect]:
        diff = abs(p1.longitude - p2.longitude)
        if diff > 180: diff = 360 - diff
        
        for name, angle in angles.items():
            orb_limit = orbs.get(name, 0.0)
            actual_orb = abs(diff - angle)
            
            if actual_orb <= orb_limit:
                 # Calculate applying/separating logic (same as before)
                 # ... (Moving pure math here)
                 
                angular_diff = (p2.longitude - p1.longitude + 180) % 360 - 180
                relative_speed = p2.speed_long - p1.speed_long
                
                is_applying = False
                if angle == 0.0:
                    is_applying = (angular_diff > 0 and relative_speed < 0) or \
                                  (angular_diff < 0 and relative_speed > 0)
                elif angle == 180.0:
                    if angular_diff > 0:
                        is_applying = relative_speed < 0 and angular_diff < 180
                    else:
                        is_applying = relative_speed > 0 and angular_diff > -180
                else:
                    target_angle = angle if angular_diff > 0 else -angle
                    if angular_diff > 0:
                        is_applying = relative_speed < 0
                    else:
                        is_applying = relative_speed > 0
                 
                return Aspect(
                    p1=p1.planet,
                    p2=p2.planet,
                    angle=diff,
                    orb=actual_orb,
                    type=name,
                    applying=is_applying
                )
        return None
