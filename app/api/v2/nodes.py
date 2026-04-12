"""
/api/v2/nodes — Lunar nodes, Lilith, and planetary nodes/apsides.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet
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

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/lunar",
    response_model=LunarNodesResponse,
    summary="Get North and South lunar node positions",
)
def get_lunar_nodes(
    time: datetime = Query(...),
    true_node: bool = Query(True, description="True node (oscillating) vs Mean node"),
    context: CalculationContext = Depends(get_calculation_context),
) -> LunarNodesResponse:
    """
    Calculate the True or Mean North and South lunar nodes.
    """
    t = Time(time)
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
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="astronomy.nodes.lunar"
        ),
        data=data
    )


@router.get(
    "/lilith",
    response_model=LilithResponse,
    summary="Get Black Moon Lilith position",
)
def get_lilith(
    time: datetime = Query(...),
    true_lilith: bool = Query(False, description="True (oscillating) vs Mean Lilith"),
    context: CalculationContext = Depends(get_calculation_context),
) -> LilithResponse:
    """
    Calculate the position of Black Moon Lilith (Mean or True).
    """
    t = Time(time)
    node_service = AstronomyNodeService(context, ephemeris=ephemeris)

    pos = node_service.get_lilith(t, true_lilith=true_lilith)

    data = LilithSchema(
        planet=pos.planet.name,
        longitude=pos.longitude,
        latitude=pos.latitude,
        is_mean=not true_lilith,
    )
    return LilithResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="astronomy.nodes.lilith"
        ),
        data=data
    )


@router.get(
    "/planetary/{planet}",
    response_model=PlanetaryNodesResponse,
    summary="Get nodes and apsides for a planet",
)
def get_planetary_nodes(
    planet: Planet,
    time: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> PlanetaryNodesResponse:
    """
    Calculate ascending/descending nodes and perihelion/aphelion for a planet.
    """
    t = Time(time)
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
    return PlanetaryNodesResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="astronomy.nodes.planetary"
        ),
        data=data
    )
