import swisseph as swe
from fastapi import APIRouter, Query

from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...schemas.astro import (
    EphemerisStatusData,
    EphemerisStatusResponse,
    PlanetPositionData,
    PlanetPositionResponse,
)
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/ephemeris-status",
    response_model=EphemerisStatusResponse,
    summary="Get Swiss Ephemeris status",
)
async def get_ephemeris_status() -> EphemerisStatusResponse:
    """
    Get the current status of the Swiss Ephemeris engine and its data path.
    """
    swe_v = swe.version
    ephe_p = ephemeris.ephe_path

    data = EphemerisStatusData(status="online", swe_version=swe_v, ephe_path=ephe_p)

    return EphemerisStatusResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)


@router.get(
    "/planet/{planet}",
    response_model=PlanetPositionResponse,
    summary="Get single planet telemetry",
)
async def get_planet_position(
    planet: Planet,
    time: str = Query(...),
    sidereal: bool = Query(True),
    sidereal_mode: SiderealMode = Query(SiderealMode.LAHIRI),
) -> PlanetPositionResponse:
    """
    Calculate high-precision telemetry for a single celestial body.
    """
    t = Time.from_string(time)
    pos = ephemeris.calculate_planet(t.julian_day, planet, sidereal=sidereal)

    # Convert raw dict from ephemeris to PlanetPositionData
    data = PlanetPositionData(
        planet=planet.name,
        longitude=pos["longitude"],
        latitude=pos["latitude"],
        distance=pos["distance"],
        speed_long=pos["speed_long"],
        is_retrograde=pos["speed_long"] < 0,
        sign=int(pos["longitude"] / 30) + 1,
        sign_name=PlanetPositionData.get_sign_name(pos["longitude"]),
    )

    return PlanetPositionResponse(
        meta=get_meta(is_sidereal=sidereal, sidereal_mode=sidereal_mode), data=data
    )
