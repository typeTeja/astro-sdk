from pydantic import BaseModel, Field, field_validator

from ..core.constants import Planet
from .settings import ChartSettings


class AspectSchema(BaseModel):
    """
    Standardized response for a single astrological aspect.
    """

    p1: Planet
    p2: Planet
    type: str = Field(..., description="conjunction, square, trine, etc.")
    angle: float = Field(..., description="Exact angular difference")
    orb: float = Field(..., description="Remaining orb from exactitude")
    is_applying: bool


class AspectRequest(BaseModel):
    """
    Request parameters for aspect calculation.
    """

    time: AstroTimeInput
    location: GeographicLocation | None = None
    settings: ChartSettings = Field(default_factory=ChartSettings)

    planets: list[Planet] | None = Field(
        None, description="Filter which planets to include in calculation"
    )
    aspect_types: list[str] | None = Field(
        None, description="Filter aspect types (major, minor, etc.)"
    )
    global_orb: float | None = Field(
        None, ge=0, le=12, description="Global fallback orb for all aspects"
    )
    custom_orbs: dict[str, float] | None = Field(
        None, description="Override orbs per aspect type (e.g., {'CONJUNCTION': 8.0})"
    )

    @field_validator("custom_orbs")
    @classmethod
    def validate_orbs(cls, v: dict[str, float] | None) -> dict[str, float] | None:
        if v is None:
            return v
        for aspect, orb in v.items():
            if orb < 0:
                raise ValueError(f"Orb for {aspect} cannot be negative")
            if orb > 15:
                raise ValueError(f"Orb for {aspect} exceeds maximum allowed (15.0)")
        return v


class AspectResponse(BaseAstroResponse[list[AspectSchema]]):
    """
    Standardized response envelope for a list of aspects.
    """

    pass
