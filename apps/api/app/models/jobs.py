from app.core.clock import get_current_time
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from sqlmodel import JSON, Column, Field, SQLModel


class JobStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Job(SQLModel, table=True):
    """
    Persistent record for tracking background tasks like large exports or scans.
    """

    id: int | None = Field(default=None, primary_key=True)
    task_type: str = Field(..., description="EXPORT, SCAN, RESEARCH")
    status: JobStatus = Field(default=JobStatus.PENDING)

    # Store arbitrary payload/params for the job
    payload: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    result_url: str | None = Field(None, description="Path or URL to the generated result")
    error_message: str | None = Field(None)

    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)
    completed_at: datetime | None = Field(None)
