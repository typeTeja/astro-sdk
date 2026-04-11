from ... import __version__
from ...core.constants import HouseSystem, SiderealMode
from ...schemas.base import AstroMeta


def get_meta(
    is_sidereal: bool = True,
    sidereal_mode: SiderealMode | None = SiderealMode.LAHIRI,
    heliocentric: bool = False,
    house_system: HouseSystem = HouseSystem.WHOLE_SIGN,
    astro_data_only: bool | None = None,
    no_financial_advice: bool | None = None,
    experimental: bool | None = None,
    algorithm_status: str | None = None,
    requires_domain_validation: bool | None = None,
    capability: str | None = None,
    feature_maturity: str | None = None,
    calculation_fingerprint: str | None = None,
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
        astro_data_only=astro_data_only,
        no_financial_advice=no_financial_advice,
        experimental=experimental,
        algorithm_status=algorithm_status,
        requires_domain_validation=requires_domain_validation,
        capability=capability,
        feature_maturity=feature_maturity,
        calculation_fingerprint=calculation_fingerprint,
        engine_version=__version__,
    )
