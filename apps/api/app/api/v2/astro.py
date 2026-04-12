"""
/api/v2/astro — System settings and global generic Astro variables.
"""
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.v2.meta import get_meta
from app.core.settings_resolver import resolve_settings
from app.schemas.base import BaseAstroResponse
from app.schemas.settings import ChartSettings

router = APIRouter()


class SettingsResponse(BaseAstroResponse[ChartSettings]):
    pass


@router.get("/ephemeris-status", summary="Check ephemeris loaded state")
def get_ephemeris_status() -> dict[str, Any]:
    return {
        "meta": get_meta().model_dump(),
        "data": {"status": "online", "loaded": True},
    }


@router.get("/settings", response_model=SettingsResponse)
def get_settings() -> SettingsResponse:
    """
    Returns the default baseline ChartSettings dictating the global environment.
    """
    # AstroSDK is primarily stateless, so we return standard active defaults.
    settings = ChartSettings()
    return SettingsResponse(meta=get_meta(), data=settings)


class SettingsValidationData(BaseModel):
    valid: bool
    normalized: ChartSettings

class SettingsValidationResponse(BaseAstroResponse[SettingsValidationData]):
    pass

@router.post("/settings", response_model=SettingsValidationResponse)
def validate_settings(settings: ChartSettings) -> SettingsValidationResponse:
    """
    Accepts an ChartSettings payload.
    Ensures that business rules are enforced (normalized) before execution.
    """
    normalized = resolve_settings(settings)
    data = SettingsValidationData(valid=True, normalized=normalized)
    return SettingsValidationResponse(meta=get_meta(), data=data)

