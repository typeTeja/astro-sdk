from app.contexts.calculation import CalculationContext
from app.contexts.coordinate import CoordinateContext, CoordinateSystem
from app.contexts.feature import FeatureContext, FeatureMaturity
from app.contexts.house import HouseContext
from app.contexts.observer import ObserverContext
from app.contexts.zodiac import ZodiacContext, ZodiacType
from app.core.constants import HouseSystem, SiderealMode


def build_western_chart_context(
    *,
    house_system: HouseSystem = HouseSystem.WHOLE_SIGN,
    sidereal_mode: SiderealMode | None = SiderealMode.LAHIRI,
    is_sidereal: bool = True,
    heliocentric: bool = False,
    latitude: float | None = None,
    longitude: float | None = None,
    altitude: float = 0.0,
    capability: str = "western.chart",
    maturity: FeatureMaturity = FeatureMaturity.BETA,
) -> CalculationContext:
    zodiac = ZodiacContext(
        zodiac=ZodiacType.SIDEREAL if is_sidereal else ZodiacType.TROPICAL,
        sidereal_mode=sidereal_mode if is_sidereal else None,
    )
    coordinate = CoordinateContext(
        system=CoordinateSystem.HELIOCENTRIC if heliocentric else CoordinateSystem.GEOCENTRIC
    )
    observer = None
    if latitude is not None and longitude is not None:
        observer = ObserverContext(
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
        )

    return CalculationContext(
        zodiac=zodiac,
        coordinate=coordinate,
        house=HouseContext(system=house_system),
        observer=observer,
        feature=FeatureContext(capability=capability, maturity=maturity),
    )


def create_default_context() -> CalculationContext:
    """Create a minimal default context for internal migration logic."""
    return CalculationContext(
        zodiac=ZodiacContext(zodiac=ZodiacType.SIDEREAL, sidereal_mode=SiderealMode.LAHIRI),
        coordinate=CoordinateContext(system=CoordinateSystem.GEOCENTRIC),
        house=HouseContext(system=HouseSystem.WHOLE_SIGN),
        feature=FeatureContext(capability="core.generic", maturity=FeatureMaturity.EXPERIMENTAL),
    )
