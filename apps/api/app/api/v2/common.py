from typing import Annotated

from fastapi import Header, HTTPException, Query

from app.contexts.calculation import CalculationContext
from app.contexts.factories import create_default_context
from app.core.constants import HouseSystem, SiderealMode, validate_enum_by_name


def get_calculation_context(
    # Header-based context overrides
    house_system: Annotated[str | None, Header(alias="X-Astro-House-System")] = None,
    sidereal_mode: Annotated[str | None, Header(alias="X-Astro-Sidereal-Mode")] = None,
    is_sidereal: Annotated[bool | None, Header(alias="X-Astro-Is-Sidereal")] = None,
    heliocentric: Annotated[bool | None, Header(alias="X-Astro-Heliocentric")] = None,
    coordinate_system: Annotated[str | None, Header(alias="X-Astro-Coordinate-System")] = None,
    lat: Annotated[float | None, Header(alias="X-Astro-Latitude")] = None,
    lon: Annotated[float | None, Header(alias="X-Astro-Longitude")] = None,
    alt: Annotated[float | None, Header(alias="X-Astro-Altitude")] = None,

    # Query-based context overrides
    q_house_system: Annotated[str | None, Query(alias="house_system")] = None,
    q_sidereal_mode: Annotated[str | None, Query(alias="sidereal_mode")] = None,
    q_is_sidereal: Annotated[bool | None, Query(alias="is_sidereal")] = None,
    q_coordinate_system: Annotated[str | None, Query(alias="coordinate_system")] = None,
    q_lat: Annotated[float | None, Query(alias="latitude")] = None,
    q_lon: Annotated[float | None, Query(alias="longitude")] = None,
    q_alt: Annotated[float | None, Query(alias="altitude")] = None,
) -> CalculationContext:
    """
    FastAPI dependency to build a 2.0 CalculationContext from headers and query params.
    Supports Topocentric, Heliocentric, and Geocentric systems with optional observer data.
    """
    ctx = create_default_context()

    # 1. Determine Coordinate System (Moved up for validation)
    from app.contexts.coordinate import CoordinateSystem
    final_sys_raw = coordinate_system or q_coordinate_system
    system = CoordinateSystem.GEOCENTRIC
    if final_sys_raw:
        system = CoordinateSystem(final_sys_raw.lower())
    elif heliocentric is not None:
        system = CoordinateSystem.HELIOCENTRIC if heliocentric else CoordinateSystem.GEOCENTRIC
    
    ctx.coordinate.system = system

    # 2. Extract Observer Coordinates
    final_lat = lat if lat is not None else q_lat
    final_lon = lon if lon is not None else q_lon
    final_alt = alt if alt is not None else q_alt

    # 3. Strict Validation for Topocentric
    if system == CoordinateSystem.TOPOCENTRIC:
        if final_lat is None or final_lon is None:
            raise HTTPException(
                status_code=400,
                detail="Topocentric calculations require explicit latitude and longitude."
            )

    # 4. Initialize Observer (if valid coordinates provided)
    if final_lat is not None or final_lon is not None:
        from app.contexts.observer import ObserverContext
        ctx.observer = ObserverContext(
            latitude=final_lat or 0.0,
            longitude=final_lon or 0.0,
            altitude=final_alt or 0.0
        )
    # Observer remains None if no coords provided (Geocentric case)

    # 5. Houses & Sidereal Mode
    final_house_raw = house_system or q_house_system
    if final_house_raw:
        ctx.house.system = HouseSystem(final_house_raw.upper()) if not final_house_raw.isdigit() else HouseSystem(final_house_raw)

    final_sid_mode_raw = sidereal_mode or q_sidereal_mode
    if final_sid_mode_raw:
        ctx.zodiac.sidereal_mode = validate_enum_by_name(SiderealMode, final_sid_mode_raw)

    # 6. Zodiac Type
    final_is_sidereal = is_sidereal if is_sidereal is not None else q_is_sidereal
    if final_is_sidereal is not None:
        from app.contexts.zodiac import ZodiacType
        ctx.zodiac.zodiac = ZodiacType.SIDEREAL if final_is_sidereal else ZodiacType.TROPICAL

    return ctx
