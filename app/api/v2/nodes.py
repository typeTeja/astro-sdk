"""
/api/v2/nodes — Lunar nodes, Lilith, and planetary nodes/apsides.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.nodes import (
    LilithResponse,
    LilithSchema,
    LunarNodesResponse,
    LunarNodesSchema,
    NodePositionSchema,
    PlanetaryNodesResponse,
    PlanetaryNodesSchema,
)
from app.services.astronomy.node_service import AstronomyNodeService
from app.contexts.factories import create_default_context
from app.api.v2.meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/lunar",
    response_model=LunarNodesResponse,
    summary="Get North and South lunar node positions",
)
async def get_lunar_nodes(
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    true_node: bool = Query(True, description="True node (oscillating) vs Mean node"),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> LunarNodesResponse:
    """
    Calculate the True or Mean North and South lunar nodes.
    """
    t = Time(time)
    context = create_default_context()
    context.zodiac.sidereal_mode = sidereal_mode
    node_service = AstronomyNodeService(context, ephemeris=ephemeris)
    
    north, south = node_service.get_lunar_nodes(t, true_node=true_node)

    node_label = "True Node" if true_node else "Mean Node"
    data = LunarNodesSchema(
        north_node=NodePositionSchema(
            body=f"North {node_label}",
            longitude=north.longitude,
            latitude=north.latitude,
        ),
        south_node=NodePositionSchema(
            body=f"South {node_label}",
            longitude=south.longitude,
            latitude=south.latitude,
        ),
    )
    return LunarNodesResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode), data=data
    )


@router.get(
    "/lilith",
    response_model=LilithResponse,
    summary="Get Black Moon Lilith position",
)
async def get_lilith(
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    true_lilith: bool = Query(False, description="True (oscillating) vs Mean Lilith"),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> LilithResponse:
    """
    Calculate the position of Black Moon Lilith (Mean or True).
    """
    t = Time(time)
    context = create_default_context()
    context.zodiac.sidereal_mode = sidereal_mode
    node_service = AstronomyNodeService(context, ephemeris=ephemeris)
    
    pos = node_service.get_lilith(t, true_lilith=true_lilith)

    data = LilithSchema(
        planet=pos.planet.name,
        longitude=pos.longitude,
        latitude=pos.latitude,
        is_mean=not true_lilith,
    )
    return LilithResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode), data=data
    )


@router.get(
    "/planetary/{planet}",
    response_model=PlanetaryNodesResponse,
    summary="Get nodes and apsides for a planet",
)
async def get_planetary_nodes(
    planet: Planet,
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
) -> PlanetaryNodesResponse:
    """
    Calculate ascending/descending nodes and perihelion/aphelion for a planet.
    """
    t = Time(time)
    # Binary search for nodes/apsides is mostly tropical/neutral in SE
    context = create_default_context()
    node_service = AstronomyNodeService(context, ephemeris=ephemeris)
    
    nodes = node_service.get_planetary_nodes(t, planet)
    apsides = node_service.get_apsides(t, planet)

    data = PlanetaryNodesSchema(
        planet=planet.name,
        ascending_node=nodes["ascending_node"],
        descending_node=nodes["descending_node"],
        perihelion=apsides["perihelion"],
        aphelion=apsides["aphelion"],
    )
    return PlanetaryNodesResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)
