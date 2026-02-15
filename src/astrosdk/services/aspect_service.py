from typing import List, Optional
from ..domain.planet import PlanetPosition
from ..domain.aspect import Aspect
from ..core.constants import Planet

class AspectService:
    """
    Calculates aspects between planets.
    """
    
    DEFAULT_ORBS = {
        "CONJUNCTION": 8.0,
        "SQUARE": 7.0,
        "TRINE": 8.0,
        "OPPOSITION": 8.0,
        "SEXTILE": 5.0
    }
    
    ASPECT_ANGLES = {
        0.0: "CONJUNCTION",
        90.0: "SQUARE",
        120.0: "TRINE",
        180.0: "OPPOSITION",
        60.0: "SEXTILE"
    }

    def calculate_aspects(self, planets: List[PlanetPosition]) -> List[Aspect]:
        results = []
        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                aspect = self.get_aspect(p1, p2)
                if aspect:
                    results.append(aspect)
        return results

    def get_aspect(self, p1: PlanetPosition, p2: PlanetPosition) -> Optional[Aspect]:
        diff = abs(p1.longitude - p2.longitude)
        if diff > 180:
            diff = 360 - diff
            
        for angle, name in self.ASPECT_ANGLES.items():
            orb_limit = self.DEFAULT_ORBS.get(name, 0.0)
            actual_orb = abs(diff - angle)
            
            if actual_orb <= orb_limit:
                # Determine applying/separating based on relative velocity
                # An aspect is "applying" if the planets are moving closer to exactitude
                # An aspect is "separating" if the planets are moving away from exactitude
                
                # Calculate the rate of change of the aspect angle
                # If the faster planet is "catching up" to form the aspect, it's applying
                # If the faster planet is "moving away" from the aspect, it's separating
                
                # Normalize the angular difference to -180 to 180
                angular_diff = (p2.longitude - p1.longitude + 180) % 360 - 180
                
                # Relative speed (how fast p2 is moving relative to p1)
                relative_speed = p2.speed_long - p1.speed_long
                
                # For each aspect type, determine if we're approaching or separating
                # The aspect is applying if the relative motion reduces the orb
                if angle == 0.0:  # Conjunction
                    # Moving toward 0° separation
                    is_applying = (angular_diff > 0 and relative_speed < 0) or \
                                  (angular_diff < 0 and relative_speed > 0)
                elif angle == 180.0:  # Opposition
                    # Moving toward 180° separation
                    if angular_diff > 0:
                        is_applying = relative_speed < 0 and angular_diff < 180
                    else:
                        is_applying = relative_speed > 0 and angular_diff > -180
                else:  # Other aspects (60, 90, 120)
                    # Check if relative motion is reducing the orb
                    # If angular_diff is close to +angle, and relative_speed is negative, applying
                    # If angular_diff is close to -angle, and relative_speed is positive, applying
                    target_angle = angle if angular_diff > 0 else -angle
                    distance_to_exact = abs(angular_diff) - angle
                    
                    # If distance is decreasing, it's applying
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
