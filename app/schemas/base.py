from datetime import UTC, datetime
from typing import TypeVar

from pydantic import BaseModel, Field, field_validator

from ..core.constants import HouseSystem, SiderealMode

T = TypeVar("T")


class GeographicLocation(BaseModel):
    """
    Coordinates for the observer.
    """

    latitude: float = Field(
        ..., ge=-90, le=90, description="Latitude in decimal degrees (-90 to 90)"
    )
    longitude: float = Field(
        ..., ge=-180, le=180, description="Longitude in decimal degrees (-180 to 180)"
    )
    altitude: float = Field(0.0, description="Altitude in meters above sea level")


class AstroSettings(BaseModel):
    """
    Control settings for the astronomical engine.
    Strictly follows User Rule 8 for defaults.
    """

    sidereal_mode: SiderealMode | None = Field(
        default=SiderealMode.LAHIRI,
        description="Ayanamsa system (only used if is_sidereal is True)",
    )
    house_system: HouseSystem = Field(
        default=HouseSystem.WHOLE_SIGN, description="House system for cusp calculation"
    )
    is_sidereal: bool = Field(
        default=True, description="Whether to use sidereal (True) or tropical (False) zodiac"
    )


class AstroTimeInput(BaseModel):
    """
    Normalized time input for all endpoints.
    Requires ISO format with timezone info.
    """

    time: datetime = Field(
        ..., description="ISO 8601 formatted datetime with timezone (e.g., 2024-01-01T12:00:00Z)"
    )

    @field_validator("time")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError(
                "Naive datetime not allowed. Must include timezone offset (e.g., +05:30 or Z)"
            )
        return v.astimezone(UTC)


class AstroMeta(BaseModel):
    """
    Standardized metadata block for all API responses.
    Ensures total transparency of the calculation context.
    """

    zodiac: str = Field(..., description="Zodiac used (sidereal or tropical)")
    ayanamsa: str | None = Field(None, description="Ayanamsa system used (if sidereal)")
    house_system: str = Field(..., description="House system used")
    coordinate_system: str = Field(..., description="geocentric or heliocentric")
    calculation_time: str = "UTC"


class BaseAstroResponse[T](BaseModel):
    """
    Standardized envelope for all API responses.
    """

    meta: AstroMeta
    data: T
