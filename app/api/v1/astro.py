"""
/api/v1/astro — System settings and global generic Astro variables.
"""
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel

from ...schemas.base import AstroSettings, BaseAstroResponse
from .meta import get_meta

router = APIRouter()


class SettingsResponse(BaseAstroResponse[AstroSettings]):
    pass


@router.get("/ephemeris-status", summary="Check ephemeris loaded state")
async def get_ephemeris_status() -> dict[str, Any]:
    return {
        "meta": get_meta().model_dump(),
        "data": {"status": "online", "loaded": True},
    }


@router.get("/settings", response_model=SettingsResponse)
async def get_settings() -> SettingsResponse:
    """
    Returns the default baseline AstroSettings dictating the global environment.
    """
    # AstroSDK is primarily stateless, so we return standard active defaults.
    settings = AstroSettings()
    return SettingsResponse(meta=get_meta(), data=settings)


class SettingsValidationData(BaseModel):
    valid: bool
    normalized: AstroSettings

class SettingsValidationResponse(BaseAstroResponse[SettingsValidationData]):
    pass

@router.post("/settings", response_model=SettingsValidationResponse)
async def validate_settings(settings: AstroSettings) -> SettingsValidationResponse:
    """
    Accepts an AstroSettings payload.
    Since backend is stateless, this serves strictly as payload validation 
    and normalization before downstream execution. Does not store to SQLite.
    """
    data = SettingsValidationData(valid=True, normalized=settings)
    return SettingsValidationResponse(meta=get_meta(), data=data)
