from app.core.clock import get_current_time
from datetime import UTC, datetime
from typing import Any

from sqlmodel import JSON, Column, Field, SQLModel


class UserPreset(SQLModel, table=True):
    """
    Persistent calculation settings (e.g., 'Modern Western', 'Traditional Vedic').
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., unique=True)

    # Complete serialized CalculationContext
    configuration: dict[str, Any] = Field(..., sa_column=Column(JSON))

    is_default: bool = Field(default=False)
    created_at: datetime = Field(default_factory=get_current_time)
