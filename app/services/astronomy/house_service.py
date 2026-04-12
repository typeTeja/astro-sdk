from app.contexts import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.astronomy.house import ChartHouses, HouseAxes, HouseCusp
from app.domain.common.metadata import DomainMetadata


class AstronomyHouseService:
    """AstroSDK 2.0 service for house calculation."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def calculate_houses(
        self,
        time: Time,
        lat: float,
        lon: float,
    ) -> ChartHouses:
        """Calculates house cusps and axes using the current context."""
        house_ctx = self.context.house
        zodiac_ctx = self.context.zodiac

        data = self._eph.calculate_houses(
            time.julian_day,
            lat,
            lon,
            system=house_ctx.system,
            sidereal=zodiac_ctx.is_sidereal
        )

        cusps = [
            HouseCusp(number=i+1, longitude=lon)
            for i, lon in enumerate(data["cusps"])
        ]

        axes = HouseAxes(
            ascendant=data["ascendant"],
            midheaven=data["mc"],
            descendant=(data["ascendant"] + 180) % 360,
            imum_coeli=(data["mc"] + 180) % 360,
            vertex=data["vertex"]
        )

        return ChartHouses(
            system=house_ctx.system,
            cusps=cusps,
            axes=axes,
            metadata=DomainMetadata(
                capability="astronomy.houses",
                maturity=self.context.feature.maturity.value,
                fingerprint=self.context.fingerprint
            )
        )
