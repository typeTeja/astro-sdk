from typing import Annotated

from fastapi import Depends, Header, Query, Request

from app.contexts.calculation import CalculationContext
from app.contexts.factories import create_default_context
from app.core.constants import HouseSystem, SiderealMode, validate_enum_by_name
from app.core.settings_resolver import resolve_settings
from app.schemas.settings import ChartSettings


def get_merged_settings(
    # Header-based context overrides
    house_system: Annotated[str | None, Header(alias="X-Astro-House-System")] = None,
    sidereal_mode: Annotated[str | None, Header(alias="X-Astro-Sidereal-Mode")] = None,
    is_sidereal: Annotated[bool | None, Header(alias="X-Astro-Is-Sidereal")] = None,
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
) -> ChartSettings:
    """
    FastAPI dependency to merge inputs from headers and query parameters into a base ChartSettings.
    Priority: Header > Query > Default.
    """
    # 1. Coordinate System
    final_coord = coordinate_system or q_coordinate_system or "geocentric"
    if lat is not None or lon is not None or q_lat is not None or q_lon is not None:
        # If any coords are provided, we default to topocentric if not explicitly helio/geo
        if final_coord == "geocentric":
            final_coord = "topocentric"

    # 2. Sidereal vs Tropical
    final_is_sidereal = is_sidereal if is_sidereal is not None else q_is_sidereal
    zodiac = "sidereal" if final_is_sidereal is not False else "tropical"

    # 3. Sidereal Mode (Ayanamsa)
    final_sid_mode = None
    sid_mode_raw = sidereal_mode or q_sidereal_mode
    if sid_mode_raw:
        final_sid_mode = validate_enum_by_name(SiderealMode, sid_mode_raw)

    # 4. House System
    final_house = None
    house_raw = house_system or q_house_system
    if house_raw:
        final_house = HouseSystem(house_raw.upper()) if not house_raw.isdigit() else HouseSystem(house_raw)

    return ChartSettings(
        zodiac=zodiac,
        sidereal_mode=final_sid_mode,
        house_system=final_house or HouseSystem.WHOLE_SIGN,
        coordinate_system=final_coord
    )


def get_calculation_context(
    merged: Annotated[ChartSettings, Depends(get_merged_settings)]
) -> CalculationContext:
    """
    Final dependency that resolves settings and produces a CalculationContext.
    This ensures that 100% of inputs pass through the deterministic resolver.
    """
    resolved = resolve_settings(merged)
    ctx = create_default_context()
    ctx.apply_settings(resolved)
    return ctx


