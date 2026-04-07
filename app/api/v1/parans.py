"""
/api/v1/parans — Simultaneous horizon/meridian events (Parans).
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Query

from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.parans import ParanResponse, ParanSchema
from ...services.paran_service import ParanService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()
paran_service = ParanService(ephemeris)


@router.get(
    "/",
    response_model=ParanResponse,
    summary="Find parans for a given date and location",
)
async def get_parans(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    altitude: float = Query(0.0, description="Observer altitude in metres"),
    time: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    orb_minutes: float = Query(5.0, gt=0.0, le=60.0, description="Orb in arc-minutes"),
) -> ParanResponse:
    """
    Find all parans (simultaneous angular coincidences between planets) for a given day.
    A paran occurs when two planets simultaneously hit the horizon or meridian angles.
    """
    t = Time(time)
    raw = paran_service.find_parans(t, latitude, longitude, altitude, orb_minutes)

    data = [
        ParanSchema(
            p1=r["p1"].name,
            event1=r["type1"],
            p2=r["p2"].name,
            event2=r["type2"],
            time=r["time"].dt,
            orb_minutes=r["orb_minutes"],
        )
        for r in raw
    ]
    return ParanResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)
