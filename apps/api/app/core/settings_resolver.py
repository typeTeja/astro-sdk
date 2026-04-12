from app.schemas.settings import ChartSettings


def resolve_settings(settings: ChartSettings) -> ChartSettings:
    """
    Deterministic resolver that enforces all astrology business rules.
    This is the SOLE source of truth for configuration logic in AstroSDK.
    """

    # 1. Zodiac vs Ayanamsa Enforcement
    if settings.zodiac == "tropical":
        # Tropical zodiac does not use an ayanamsa.
        settings.sidereal_mode = None
    elif settings.zodiac == "sidereal":
        # Sidereal calculations MANDATE an ayanamsa.
        if settings.sidereal_mode is None:
            from app.core.constants import DEFAULT_SIDEREAL
            settings.sidereal_mode = DEFAULT_SIDEREAL

    # 2. Coordinate System Normalization
    if settings.coordinate_system == "heliocentric":
        # Heliocentric calculations are observer-independent.
        # House systems and observer location are irrelevant.
        settings.house_system = None

    # 3. Aspect System Rules
    if settings.aspect_system is None:
        # If no aspect system is active, orbs have no meaning.
        settings.orb = None

    return settings


def resolve_calculation_context(context: "CalculationContext") -> None:
    """
    In-place resolution for an existing CalculationContext.
    Ensures that business rules are enforced even after multiple merges.
    """
    from app.contexts.zodiac import ZodiacType

    # 1. Zodiac vs Ayanamsa
    if context.zodiac.zodiac == ZodiacType.TROPICAL:
        context.zodiac.sidereal_mode = None
    elif context.zodiac.zodiac == ZodiacType.SIDEREAL:
        if context.zodiac.sidereal_mode is None:
            from app.core.constants import DEFAULT_SIDEREAL
            context.zodiac.sidereal_mode = DEFAULT_SIDEREAL

    # 2. Coordinate System Normalization
    from app.contexts.coordinate import CoordinateSystem
    if context.coordinate.system == CoordinateSystem.HELIOCENTRIC:
        # House systems are irrelevant in heliocentric
        context.house.system = None

