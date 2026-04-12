from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BeforeValidator

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.constants import Planet, validate_enum_by_name
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.quant import (
    AstroIndicatorResponse,
    AstroIndicatorSchema,
    SynodicEventResponse,
    SynodicEventSchema,
    SynodicPhaseResponse,
    SynodicPhaseSchema,
)
from app.services.astronomy.synodic_service import AstronomySynodicService
from app.services.research.quant_service import ResearchQuantService

router = APIRouter()
ephemeris = Ephemeris()

# Specialized Type with BeforeValidator for API parameters
PlanetParam = Annotated[
    Planet, Depends(lambda v: validate_enum_by_name(Planet, v))
]  # Use Depends for query params or simple Annotated for body

# Actually, for Query params in FastAPI, we use Annotated[Planet, Query(...)]
# But our validator needs to run. BeforeValidator is standard Pydantic.
PlanetQuery = Annotated[Planet, BeforeValidator(lambda v: validate_enum_by_name(Planet, v))]


@router.get(
    "/synodic/phase", response_model=SynodicPhaseResponse, summary="Get synodic cycle phase"
)
def get_synodic_phase(
    p1: PlanetQuery,
    p2: PlanetQuery,
    time: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> SynodicPhaseResponse:
    """
    Calculate the relative angular phase (0-360°) between two planets.
    """
    t = Time(time)
    quant_service = ResearchQuantService(context, ephemeris=ephemeris)
    res = quant_service.calculate_synodic_phase(p1, p2, t)

    return SynodicPhaseResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="research.quant.synodic"
        ),
        data=SynodicPhaseSchema(
            p1=p1.name, p2=p2.name, phase=res.phase, is_applying=res.is_applying
        ),
    )


@router.get(
    "/synodic/next",
    response_model=SynodicEventResponse,
    summary="Find next synodic event",
)
def get_next_synodic_event(
    p1: PlanetQuery,
    p2: PlanetQuery,
    target_angle: float = Query(0.0),
    time: datetime = Query(...),
    max_days: float = Query(1000.0),
    context: CalculationContext = Depends(get_calculation_context),
) -> SynodicEventResponse:
    """
    Find the next occurrence of a specific synodic angle (e.g., 0°=Conjunction).
    """
    t = Time(time)
    synodic_service = AstronomySynodicService(context, ephemeris=ephemeris)
    res = synodic_service.find_next_event(p1, p2, t, target_angle, max_days)

    if not res:
        return SynodicEventResponse(
            meta=get_meta(is_sidereal=False, sidereal_mode=None),
            data=None,  # type: ignore[arg-type]
        )

    return SynodicEventResponse(
        meta=get_meta(is_sidereal=False, sidereal_mode=None),
        data=SynodicEventSchema(
            p1=res["p1"], p2=res["p2"], time=res["time"], angle=res["target_angle"]
        ),
    )


@router.get(
    "/indicators", response_model=AstroIndicatorResponse, summary="Get quantitative indicators"
)
def get_indicators(
    time: datetime = Query(...),
    planets: list[PlanetQuery] | None = Query(None),
    context: CalculationContext = Depends(get_calculation_context),
) -> AstroIndicatorResponse:
    """
    Generate planetary indicator set for a specific moment.
    """
    t = Time(time)
    quant_service = ResearchQuantService(context, ephemeris=ephemeris)

    if not planets:
        planets = [Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS, Planet.MARS]

    # Calculate indicators
    res_dict: dict[str, float] = {}
    for p in planets:
        metrics = quant_service.get_velocity_signals(p, t)
        res_dict[f"{p.name}_velocity"] = metrics.speed
        res_dict[f"{p.name}_acceleration"] = metrics.acceleration

    return AstroIndicatorResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="research.quant.indicators"
        ),
        data=AstroIndicatorSchema(time=t.dt, indicators=res_dict),
    )
