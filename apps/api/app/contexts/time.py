from pydantic import BaseModel, Field


class TimeContext(BaseModel):
    """Precision and search tolerance preferences."""

    calculation_timezone: str = Field(default="UTC")
    tolerance_seconds: float = Field(default=1.0, gt=0.0)
    max_search_days: float | None = Field(default=None, gt=0.0)
