from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class TimeWindowSchema(BaseModel):
    """A bounded time window event."""

    planet: str
    start_time: datetime
    end_time: datetime
    event_type: str
    metadata: dict[str, str | float] = Field(default_factory=dict)


class FinancialTimeWindowData(BaseModel):
    """Wrapper around time windows with the financial disclaimer in the meta payload."""

    windows: list[TimeWindowSchema]


class FinancialTimeWindowResponse(BaseAstroResponse[FinancialTimeWindowData]):
    pass


class FinancialEventData(BaseModel):
    """Wrapper around generic events."""

    events: list[dict[str, Any]]


class FinancialEventResponse(BaseAstroResponse[FinancialEventData]):
    pass
