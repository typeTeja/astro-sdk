from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class AstroIntensitySchema(BaseModel):
    """Astronomical Intensity slice at a point in time."""

    time: datetime
    score: float = Field(..., ge=0.0, le=100.0)
    active_aspects_count: int
    top_contributors: list[dict[str, Any]]


class AstroIntensityList(BaseModel):
    intensities: list[AstroIntensitySchema]


class AstroIntensityResponse(BaseAstroResponse[AstroIntensityList]):
    pass


class ClusterSchema(BaseModel):
    """An individual planetary cluster (Stellium)."""

    center_longitude: float
    span_degrees: float
    planets: list[str]


class ClusterIndexSchema(BaseModel):
    """Density clustering across the sky."""

    time: datetime
    stellar_density_score: float
    clusters: list[ClusterSchema]


class ClusterIndexResponse(BaseAstroResponse[list[ClusterIndexSchema]]):
    pass
