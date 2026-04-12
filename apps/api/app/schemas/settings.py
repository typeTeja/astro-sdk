from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from app.core.constants import HouseSystem, SiderealMode


class ChartSettings(BaseModel):
    """
    Unified configuration schema for all AstroSDK chart generation.
    Deterministic, type-safe, and reusable across all modules.
    """

    zodiac: Literal["sidereal", "tropical"] = Field(
        default="sidereal",
        description="Zodiac system to use for calculations."
    )

    sidereal_mode: Optional[SiderealMode] = Field(
        default=SiderealMode.LAHIRI,
        description="Ayanamsa system (only used if zodiac is sidereal)."
    )

    house_system: HouseSystem = Field(
        default=HouseSystem.WHOLE_SIGN,
        description="House division system for cusp calculation."
    )

    node_type: Literal["true", "mean"] = Field(
        default="true",
        description="Lunar node calculation method."
    )

    coordinate_system: Literal["geocentric", "heliocentric", "topocentric"] = Field(
        default="geocentric",
        description="Primary coordinate system for the engine."
    )

    planets: Optional[List[str]] = Field(
        default=None,
        description="Optional filtering of specific bodies."
    )

    include_outer_planets: bool = Field(
        default=True,
        description="Whether to include Uranus, Neptune, and Pluto."
    )

    aspect_system: Optional[Literal["vedic", "western"]] = Field(
        default=None,
        description="Optional aspect calculation system."
    )

    orb: Optional[float] = Field(
        default=None,
        ge=0,
        le=12,
        description="Orb of exactitude for aspects (max 12.0)."
    )

    class Config:
        extra = "forbid"
        use_enum_values = True
