from app.core.clock import get_current_time
from datetime import UTC, datetime
from typing import Any

from sqlmodel import JSON, Column, Field, SQLModel


class SavedChart(SQLModel, table=True):
    """
    Persistent storage for birth or event charts.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., index=True)

    # Core chart data
    natal_time: datetime = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
    altitude: float = Field(default=0.0)

    # Calculation context overrides (House system, Ayanamsa, etc.)
    context_override: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # Renamed from metadata to extra_data to avoid reserved keyword conflict
    extra_data: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=get_current_time)
