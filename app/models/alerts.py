from datetime import UTC, datetime
from typing import Annotated

from pydantic import BeforeValidator
from sqlmodel import Field, SQLModel

from ..core.constants import Planet, validate_enum_by_name


class AlertRule(SQLModel, table=True):
    """
    Persistent rule for triggering astronomical notifications.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., description="User-friendly name for this alert")

    # Use Annotated with BeforeValidator for name-based coercion in Pydantic v2
    planet: Annotated[Planet, BeforeValidator(lambda v: validate_enum_by_name(Planet, v))] = Field(
        ..., description="Planet to monitor (Primary)"
    )

    secondary_planet: Annotated[
        Planet | None, BeforeValidator(lambda v: validate_enum_by_name(Planet, v))
    ] = Field(None, description="Secondary planet for aspects")

    event_type: str = Field(..., description="INGRESS, STATION, or ASPECT")
    target_value: float | None = Field(None, description="Degree, Sign ID, or Aspect Angle")

    webhook_url: str | None = Field(None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_triggered: datetime | None = Field(None)
