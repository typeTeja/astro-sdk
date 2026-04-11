from ...contexts import CalculationContext
from ...core.constants import Planet
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...domain.common.metadata import DomainMetadata


class AstronomyVisibilityService:
    """
    Native 2.0 service for visibility-related events (Heliacal rising/setting).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def calculate_heliacal_event(
        self,
        planet: Planet,
        time: Time,
        lat: float,
        lon: float,
        alt: float = 0.0,
        event_type: int = 1, # 1=rising, 2=setting etc
        star_name: str = ""
    ) -> dict:
        """
        Calculate next heliacal event for a planet or star.
        """
        res = self._eph.calculate_heliacal_event(
            time.julian_day,
            planet,
            lat,
            lon,
            alt,
            event_type=event_type,
            star_name=star_name,
        )
        
        if "event_jd" in res:
            res["time"] = Time.from_julian_day(res["event_jd"]).dt
            
        res["metadata"] = DomainMetadata(
            capability="astronomy.visibility",
            maturity=self.context.feature.maturity.value,
            fingerprint=self.context.fingerprint
        )
        
        return res
