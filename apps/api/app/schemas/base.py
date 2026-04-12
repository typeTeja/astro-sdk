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
    astro_data_only: bool | None = Field(None, description="Disclaimer: Confirms response contains pure astronomical data")
    no_financial_advice: bool | None = Field(None, description="Disclaimer: Not financial advice")
    experimental: bool | None = Field(None, description="Flags this data as deriving from a partial or experimental algorithm route.")
    algorithm_status: str | None = Field(None, description="Indicates the depth of the algorithm logic (e.g. 'partial', 'stub', 'production').")
    requires_domain_validation: bool | None = Field(None, description="Flags whether the consumer must handle geometric boundary tuning.")
    capability: str | None = Field(None, description="Canonical AstroSDK capability used for the calculation.")
    feature_maturity: str | None = Field(None, description="Maturity level of the capability used for the calculation.")
    calculation_fingerprint: str | None = Field(None, description="Deterministic fingerprint of the calculation context and primary inputs.")
    engine_version: str | None = Field(None, description="AstroSDK engine version used to produce the result.")


class BaseAstroResponse[T](BaseModel):
    """
    Standardized envelope for all API responses.
    """

    meta: AstroMeta
    data: T
