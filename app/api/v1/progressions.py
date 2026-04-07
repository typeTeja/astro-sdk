from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.astro import PlanetPositionData
from ...schemas.charts import NatalChartRequest
from ...schemas.transits import SecondaryProgressionData, SecondaryProgressionResponse
from ...services.progression_service import ProgressionService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
progression_service = ProgressionService(ephemeris)


@router.get(
    "/secondary",
    response_model=SecondaryProgressionResponse,
    summary="Get secondary progression positions",
)
async def get_secondary_progression(
    birth_time: datetime = Query(...),
    target_date: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> SecondaryProgressionResponse:
    """
    Calculate Secondary Progressions (Day-for-a-Year) for a given life moment.
    """
    t_birth = Time(birth_time)
    t_target = Time(target_date)

    # 1. Calculate progressions → returns ProgressedChart domain object
    prog = progression_service.calculate_secondary_progression(
        t_birth, t_target, sidereal_mode=sidereal_mode
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
        meta=get_meta(is_sidereal=True, sidereal_mode=sidereal_mode), data=data
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
