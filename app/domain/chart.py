from dataclasses import dataclass

from ..core.time import Time
from .house import ChartHouses
from .planet import PlanetPosition


@dataclass(frozen=True)
class Chart:
    metadata: dict[str, str]
    time: Time
    planets: list[PlanetPosition]
    houses: ChartHouses | None = None
