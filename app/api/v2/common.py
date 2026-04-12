from typing import Annotated, Any

from fastapi import Header, Query
from pydantic import AfterValidator
from app.contexts.calculation import CalculationContext
from app.contexts.factories import create_default_context
from app.core.constants import HouseSystem, SiderealMode, validate_enum_by_name


def get_calculation_context(
    # Header-based context overrides (Allow string name for convenience)
    house_system: Annotated[str | None, Header(alias="X-Astro-House-System")] = None,
    sidereal_mode: Annotated[str | None, Header(alias="X-Astro-Sidereal-Mode")] = None,
    is_sidereal: Annotated[bool | None, Header(alias="X-Astro-Is-Sidereal")] = None,
    heliocentric: Annotated[bool | None, Header(alias="X-Astro-Heliocentric")] = None,
    
    # Query-based context overrides (convenience)
    q_house_system: Annotated[str | None, Query(alias="house_system")] = None,
    q_sidereal_mode: Annotated[str | None, Query(alias="sidereal_mode")] = None,
    q_is_sidereal: Annotated[bool | None, Query(alias="is_sidereal")] = None,
) -> CalculationContext:
    """
    FastAPI dependency to build a 2.0 CalculationContext from headers and query params.
    Prioritizes headers over query params. Supports named enums (e.g., "PLACIDUS", "LAHIRI").
    """
    ctx = create_default_context()
    
    # Apply overrides with name-based validation
    final_house_raw = house_system or q_house_system
    if final_house_raw:
        ctx.house.system = HouseSystem(final_house_raw.upper()) if not final_house_raw.isdigit() else HouseSystem(final_house_raw)
        
    final_sid_mode_raw = sidereal_mode or q_sidereal_mode
    if final_sid_mode_raw:
        ctx.zodiac.sidereal_mode = validate_enum_by_name(SiderealMode, final_sid_mode_raw)
        
    if ctx.observer is None:
        from app.contexts.observer import ObserverContext
        ctx.observer = ObserverContext(latitude=0.0, longitude=0.0)
        
    final_is_sidereal = is_sidereal if is_sidereal is not None else q_is_sidereal
    if final_is_sidereal is not None:
        from app.contexts.zodiac import ZodiacType
        ctx.zodiac.zodiac = ZodiacType.SIDEREAL if final_is_sidereal else ZodiacType.TROPICAL
        
    if heliocentric is not None:
        from app.contexts.coordinate import CoordinateSystem
        ctx.coordinate.system = CoordinateSystem.HELIOCENTRIC if heliocentric else CoordinateSystem.GEOCENTRIC
        
    return ctx
