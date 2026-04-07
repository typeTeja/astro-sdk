"""Schemas for the /api/v1/nodes endpoints."""
from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class NodePositionSchema(BaseModel):
    """Lunar or planetary node / apside position."""

    body: str = Field(..., description="Node or apside identifier")
    longitude: float
    latitude: float


class LunarNodesSchema(BaseModel):
    """North and South lunar node positions."""

    north_node: NodePositionSchema
    south_node: NodePositionSchema


class LunarNodesResponse(BaseAstroResponse[LunarNodesSchema]):
    pass


class LilithSchema(BaseModel):
    """Black Moon Lilith position."""

    planet: str
    longitude: float
    latitude: float
    is_mean: bool


class LilithResponse(BaseAstroResponse[LilithSchema]):
    pass


class PlanetaryNodesSchema(BaseModel):
    """Ascending and descending nodes for a planet."""

    planet: str
    ascending_node: float
    descending_node: float
    perihelion: float
    aphelion: float


class PlanetaryNodesResponse(BaseAstroResponse[PlanetaryNodesSchema]):
    pass
