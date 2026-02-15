from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..core.constants import Planet
from ..domain.planet import PlanetaryPhenomena

class PlanetaryService:
    """
    Service for calculating planetary phenomena and advanced data.
    """
    def __init__(self):
        self._ephe = Ephemeris()

    def get_phenomena(self, planet: Planet, time: Time) -> PlanetaryPhenomena:
        """
        Calculates phenomena (magnitude, phase, etc.) for a planet.
        """
        data = self._ephe.calculate_phenomena(time.julian_day, planet)
        return PlanetaryPhenomena(
            planet=planet,
            phase_angle=data["phase_angle"],
            phase_fraction=data["phase_fraction"],
            elongation=data["elongation"],
            apparent_diameter=data["apparent_diameter"],
            apparent_magnitude=data["apparent_magnitude"]
        )
