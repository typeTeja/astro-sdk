from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.planet import FixedStarPosition


class FixedStarService:
    """
    Service for calculating fixed star positions.
    Accepts Ephemeris via dependency injection (not self-instantiated).
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self._ephe = ephemeris

    def get_star_position(
        self, star_name: str, time: Time, sidereal: bool = True
    ) -> FixedStarPosition:
        """
        Calculates the position of a fixed star.
        """
        data = self._ephe.calculate_fixed_star(time.julian_day, star_name, sidereal)
        return FixedStarPosition(
            name=data["name"],
            longitude=data["longitude"],
            latitude=data["latitude"],
            magnitude=data["magnitude"],
        )

    def get_stars_positions(
        self, star_names: list[str], time: Time, sidereal: bool = True
    ) -> list[FixedStarPosition]:
        """
        Calculates positions for multiple stars.
        """
        return [self.get_star_position(name, time, sidereal) for name in star_names]
