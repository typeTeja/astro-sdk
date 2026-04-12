from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator

from ..core.constants import Planet, validate_enum_by_name
from .base import BaseAstroResponse


class AlertRuleCreate(BaseModel):
    """
    Schema for creating a new alert rule via API.
    Decoupled from SQLModel for stricter validation control.
    """

    name: str
    planet: Annotated[Planet, BeforeValidator(lambda v: validate_enum_by_name(Planet, v))]
    secondary_planet: Annotated[
        Planet | None, BeforeValidator(lambda v: validate_enum_by_name(Planet, v))
    ] = None
    event_type: str
    target_value: float | None = None
    webhook_url: str | None = None
    is_active: bool = True


class AlertRuleData(BaseModel):
    """
    Serializable alert rule for API responses.
    """

    id: int | None = None
    name: str
    planet: str
    secondary_planet: str | None = None
    event_type: str
    target_value: float | None = None
    is_active: bool = True


class AlertRuleResponse(BaseAstroResponse[AlertRuleData]):
    pass


class AlertRuleListResponse(BaseAstroResponse[list[AlertRuleData]]):
    pass


class AlertScanResult(BaseModel):
    """
    Hit result from a scan.
    """

    rule_id: int
    name: str
    event: str
    time: Any
    details: str


class AlertScanResponse(BaseAstroResponse[list[AlertScanResult]]):
    pass
