"""
/api/v2/parans — Simultaneous horizon/meridian events (Parans).
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.parans import ParanResponse, ParanSchema
from app.services.astronomy.paran_service import AstronomyParanService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/",
    response_model=ParanResponse,
    summary="Find parans for a given date and location",
)
def get_parans(
    altitude: float = Query(0.0, description="Observer altitude in metres"),
    time: datetime = Query(...),
    orb_minutes: float = Query(5.0, gt=0.0, le=60.0, description="Orb in arc-minutes"),
    context: CalculationContext = Depends(get_calculation_context),
) -> ParanResponse:
    """
    Find all parans (simultaneous angular coincidences between planets) for a given day.
    A paran occurs when two planets simultaneously hit the horizon or meridian angles.
    """
    t = Time(time)
    paran_service = AstronomyParanService(context, ephemeris=ephemeris)
    raw = paran_service.find_parans(
        t,
        context.observer.latitude if context.observer else 0.0,
        context.observer.longitude if context.observer else 0.0,
        (context.observer.altitude if context.observer else 0.0) or altitude,
        orb_minutes,
    )

    data = [
        ParanSchema(
            p1=r["p1"],
            event1=r["type1"],
            p2=r["p2"],
            event2=r["type2"],
            time=r["time"],
            orb_minutes=r["orb_minutes"],
        )
        for r in raw
    ]
    return ParanResponse(
        meta=get_meta(
            capability="astronomy.parans",
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode
        ),
        data=data
    )
