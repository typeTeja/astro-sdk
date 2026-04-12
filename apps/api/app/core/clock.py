"""
Deterministic clock for centralized time generation.
Ensures that system-time fetches are centrally controlled and can be frozen for tests
or strictly monitored in production.
"""
from datetime import UTC, datetime
from typing import Callable

_clock_provider: Callable[[], datetime] = lambda: datetime.now(UTC)


def set_fixed_clock(fixed_time: datetime) -> None:
    """Freeze the global clock to a specific deterministic time."""
    global _clock_provider
    _clock_provider = lambda: fixed_time


def reset_clock() -> None:
    """Reset the clock back to system UTC time."""
    global _clock_provider
    _clock_provider = lambda: datetime.now(UTC)


def get_current_time() -> datetime:
    """Get the current time from the central timing provider."""
    return _clock_provider()
