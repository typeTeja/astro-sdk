"""
/api/v2/stars — Fixed star positions.
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from app.api.v2.common import get_calculation_context
from app.api.v2.meta import get_meta
from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.schemas.stars import FixedStarResponse, FixedStarSchema, FixedStarsListResponse
from app.services.astronomy.star_service import AstronomyStarService

router = APIRouter()
ephemeris = Ephemeris()


@router.get(
    "/{star_name}",
    response_model=FixedStarResponse,
    summary="Get position of a named fixed star",
)
def get_fixed_star(
    star_name: str,
    time: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> FixedStarResponse:
    """
    Calculate the ecliptic position and magnitude of a fixed star by name.
    Use Swiss Ephemeris star names (e.g., 'Aldebaran', 'Regulus', 'Spica').
    """
    t = Time(time)
    star_service = AstronomyStarService(context, ephemeris=ephemeris)

    star = star_service.get_star_position(star_name, t)

    data = FixedStarSchema(
        name=star.name,
        longitude=star.longitude,
        latitude=star.latitude,
        magnitude=star.magnitude,
    )
    return FixedStarResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="astronomy.stars"
        ),
        data=data
    )


@router.get(
    "/",
    response_model=FixedStarsListResponse,
    summary="Get positions of multiple named fixed stars",
)
def get_fixed_stars(
    star_names: list[str] = Query(..., description="Star names, e.g. Aldebaran,Regulus"),
    time: datetime = Query(...),
    context: CalculationContext = Depends(get_calculation_context),
) -> FixedStarsListResponse:
    """
    Calculate positions for a list of fixed stars in a single request.
    """
    t = Time(time)
    star_service = AstronomyStarService(context, ephemeris=ephemeris)

    stars = star_service.get_stars_positions(star_names, t)

    data = [
        FixedStarSchema(name=s.name, longitude=s.longitude, latitude=s.latitude, magnitude=s.magnitude)
        for s in stars
    ]
    return FixedStarsListResponse(
        meta=get_meta(
            is_sidereal=context.zodiac.is_sidereal,
            sidereal_mode=context.zodiac.sidereal_mode,
            capability="astronomy.stars.list"
        ),
        data=data
    )
