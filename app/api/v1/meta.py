from ...core.constants import HouseSystem, SiderealMode
from ...schemas.base import AstroMeta


def get_meta(
    is_sidereal: bool = True,
    sidereal_mode: SiderealMode | None = SiderealMode.LAHIRI,
    heliocentric: bool = False,
    house_system: HouseSystem = HouseSystem.WHOLE_SIGN,
) -> AstroMeta:
    """Standardized metadata generator for all API responses."""
    ayan_name = None
    if is_sidereal and sidereal_mode is not None:
        ayan_name = sidereal_mode.name

    return AstroMeta(
        zodiac="sidereal" if is_sidereal else "tropical",
        ayanamsa=ayan_name,
        house_system=getattr(house_system, "name", str(house_system)),
        coordinate_system="heliocentric" if heliocentric else "geocentric",
    )
