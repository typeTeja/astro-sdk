from dataclasses import dataclass

from app.core.constants import Planet
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class PlanetSnapshot:
    planet: Planet
    longitude: float
    latitude: float
    distance: float
    speed_long: float
    metadata: DomainMetadata

    @property
    def is_retrograde(self) -> bool:
        return self.speed_long < 0

    @property
    def sign(self) -> int:
        return int(self.longitude / 30)

    @property
    def sign_name(self) -> str:
        names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return names[self.sign % 12]
