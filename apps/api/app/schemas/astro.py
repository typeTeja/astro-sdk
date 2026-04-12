from pydantic import BaseModel

from .base import BaseAstroResponse


class EphemerisStatusData(BaseModel):
    """
    Current engine status and metadata.
    """

    status: str = "online"
    swe_version: str
    ephe_path: str


class EphemerisStatusResponse(BaseAstroResponse[EphemerisStatusData]):
    pass


class PlanetPositionData(BaseModel):
    """
    Telemetry for a single celestial body.
    """

    planet: str
    longitude: float
    latitude: float
    distance: float
    speed_long: float
    is_retrograde: bool
    sign: int
    sign_name: str

    @staticmethod
    def get_sign_name(lon: float) -> str:
        """Helper to get zodiac sign name from longitude."""
        signs = [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]
        return signs[int(lon / 30)]


class PlanetPositionResponse(BaseAstroResponse[PlanetPositionData]):
    pass
