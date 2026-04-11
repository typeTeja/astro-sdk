from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.transits import TransitAspectSchema, TransitScanData, TransitScanResponse
from ...engine.chart_engine import ChartEngine
from ...services.western import WesternAspectService
from ..common import build_western_chart_context, calculation_metadata
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
chart_engine = ChartEngine()


@router.get(
    "/calculate", response_model=TransitScanResponse, summary="Calculate aspects between objects"
)
async def get_aspects(
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    planets: list[Planet] | None = Query(None),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
    aspect_types: list[str] | None = Query(None),
    global_orb: float | None = Query(None),
) -> TransitScanResponse:
    """
    Search for angular interactions (aspects) between planets at a given moment.
    """
    t = Time(time)

    # Defaults
    if not planets:
        planets = [
            Planet.SUN,
            Planet.MOON,
            Planet.MERCURY,
            Planet.VENUS,
            Planet.MARS,
            Planet.JUPITER,
            Planet.SATURN,
            Planet.URANUS,
            Planet.NEPTUNE,
            Planet.PLUTO,
        ]

    # 1. Calculate positions
    chart = chart_engine.create_chart(t, lat=0, lon=0, sidereal_mode=sidereal_mode)

    # 2. Filter requested planets
    target_pos = [p for p in chart.planets if p.planet in planets]

    context = build_western_chart_context(
        sidereal_mode=sidereal_mode,
        is_sidereal=True,
        heliocentric=False,
        capability="western.aspect",
    )
    aspect_service = WesternAspectService(context)

    # 3. Scan
    matches = aspect_service.calculate_aspects(
        target_pos, aspect_types=aspect_types, global_orb=global_orb
    )
    calc_meta = calculation_metadata(
        context,
        primary_inputs={
            "time": t.dt.isoformat(),
            "planets": [planet.name for planet in planets],
            "aspect_types": aspect_types or [],
            "global_orb": global_orb,
        },
    )

    data = [
        TransitAspectSchema(
            transit_planet=m.p1.name,
            natal_planet=m.p2.name,
            aspect_type=m.type,  # Domain returns 'type', Schema expects 'aspect_type'
            angle=m.angle,
            orb=m.orb,
            is_applying=m.applying,  # Domain returns 'applying', Schema expects 'is_applying'
        )
        for m in matches
    ]

    return TransitScanResponse(
        meta=get_meta(
            is_sidereal=True,
            sidereal_mode=sidereal_mode,
            capability=calc_meta["capability"],
            feature_maturity=calc_meta["feature_maturity"],
            calculation_fingerprint=calc_meta["calculation_fingerprint"],
        ),
        data=TransitScanData(time=t.dt, aspects=data),
    )
