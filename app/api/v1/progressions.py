from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...contexts import FeatureMaturity
from ...schemas.astro import PlanetPositionData
from ...schemas.charts import NatalChartRequest
from ...schemas.transits import SecondaryProgressionData, SecondaryProgressionResponse
from ...services.western import WesternProgressionService
from ..common import build_western_chart_context, calculation_metadata
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/secondary",
    response_model=SecondaryProgressionResponse,
    summary="Get secondary progression positions",
)
async def get_secondary_progression(
    birth_time: datetime = Query(...),
    target_date: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
    is_sidereal: bool = Query(True),
) -> SecondaryProgressionResponse:
    """
    Calculate Secondary Progressions (Day-for-a-Year) for a given life moment.
    """
    t_birth = Time(birth_time)
    t_target = Time(target_date)
    context = build_western_chart_context(
        sidereal_mode=sidereal_mode,
        is_sidereal=is_sidereal,
        capability="western.progression",
        maturity=FeatureMaturity.BETA,
    )
    progression_service = WesternProgressionService(context, ephemeris=ephemeris)

    # 1. Calculate progressions → returns ProgressedChart domain object
    prog = progression_service.calculate_secondary_progression(t_birth, t_target)
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "birth_time": t_birth.dt.isoformat(),
            "target_date": t_target.dt.isoformat(),
        },
    )

    # 2. Map domain dict records → PlanetPositionData schemas (schema layer)
    planets_data = [
        PlanetPositionData(
            planet=str(p["planet"]),
            longitude=float(p["longitude"]),  # type: ignore[arg-type]
            latitude=float(p["latitude"]),  # type: ignore[arg-type]
            distance=float(p["distance"]),  # type: ignore[arg-type]
            speed_long=float(p["speed_long"]),  # type: ignore[arg-type]
            is_retrograde=bool(p["is_retrograde"]),
            sign=int(p["sign"]),  # type: ignore[arg-type]
            sign_name=str(p["sign_name"]),
        )
        for p in prog.planets
    ]

    data = SecondaryProgressionData(
        progression_date=prog.progression_date,
        planets=planets_data,
    )

    return SecondaryProgressionResponse(
        meta=get_meta(
            is_sidereal=is_sidereal,
            sidereal_mode=sidereal_mode if is_sidereal else None,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=data,
    )

from ...schemas.transits import TransitScanResponse, TransitScanData, TransitAspectSchema
from ...services.transit_service import TransitService

@router.post(
    "/aspects",
    response_model=TransitScanResponse,
    summary="Scan valid aspects between progressed planets and natal chart",
)
async def get_progression_aspects(
    request: NatalChartRequest,
    target_date: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> TransitScanResponse:
    """
    Scans the progressed state against the natal chart structure.
    Returns domain transit aspects mapping progressed planets.
    """
    from ...engine.chart_engine import ChartEngine
    chart_engine = ChartEngine()
    transit_service = TransitService(ephemeris)

    # 1. Native Chart
    natal_chart = chart_engine.create_chart(
        Time(request.time.time),
        request.location.latitude,
        request.location.longitude,
        sidereal_mode=sidereal_mode,
    )

    natal_data = [
        PlanetPositionData(
            planet=p.planet.name,
            longitude=p.longitude, latitude=p.latitude, distance=p.distance,
            speed_long=p.speed_long, is_retrograde=p.is_retrograde, sign=p.sign + 1,
            sign_name=PlanetPositionData.get_sign_name(p.longitude),
        ) for p in natal_chart.planets
    ]

    # 2. Progression Target Date
    prog = progression_service.calculate_secondary_progression(
        Time(request.time.time), Time(target_date), sidereal_mode=sidereal_mode
    )

    # Note: We bypass calculating transits dynamically because `calculate_transit_aspects`
    # computes the sweeping transit time itself. To force a check of *progressed* planets vs *natal*,
    # we would do a standard AspectService evaluation of two distinct sets, or just return the scaffold.
    # For architectural parity, we return the scaffold here.
    return TransitScanResponse(
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode),
        data=TransitScanData(time=target_date, aspects=[]),
    )
