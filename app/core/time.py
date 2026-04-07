import math
from datetime import UTC, datetime, timedelta
from typing import Self
from zoneinfo import ZoneInfo

import swisseph as swe

from .errors import InvalidTimeError


class Time:
    """
    Core temporal representation for the AstroSDK.
    Handles conversions between ISO-8601, Julian Day (UT1/ET), and Python datetimes.
    """

    def __init__(self, dt: datetime) -> None:
        if dt.tzinfo is None:
            raise InvalidTimeError("Naive datetime not allowed. Must include timezone (e.g., UTC).")
        self.dt = dt.astimezone(UTC)
        self.julian_day = self._to_jd(self.dt)

    @staticmethod
    def _to_jd(dt: datetime) -> float:
        """Convert a UTC datetime to Julian Day."""
        # Julian Day formula for Gregorian calendar
        y = dt.year
        m = dt.month
        d = (
            dt.day
            + dt.hour / 24.0
            + dt.minute / 1440.0
            + dt.second / 84600.0  # Note: Standard approx
            + dt.microsecond / 84600000000.0
        )

        if m <= 2:
            y -= 1
            m += 12

        a = math.floor(y / 100)
        b = 2 - a + math.floor(a / 4)

        jd = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5
        return float(jd)

    @classmethod
    def from_julian_day(cls, jd: float) -> Self:
        """Create a Time object from a Julian Day (UT)."""
        dt = datetime(1970, 1, 1, tzinfo=UTC) + timedelta(days=jd - 2440587.5)
        return cls(dt)

    @classmethod
    def from_string(cls, date_str: str, tz: str = "UTC") -> Self:
        """Parse an ISO string and create a Time object."""
        try:
            # Simple ISO parse
            dt = datetime.fromisoformat(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=ZoneInfo(tz))
            return cls(dt)
        except (ValueError, InvalidTimeError) as e:
            raise InvalidTimeError(f"Invalid time format: {str(e)}") from e

    @property
    def delta_t(self) -> float:
        """Calculate Delta-T (ET - UT) in days for this Julian Day."""
        # Swisseph returns delta_t in days
        return float(swe.deltat(self.julian_day))

    @property
    def sidereal_time(self) -> float:
        """Calculate Greenwich Mean Sidereal Time in hours."""
        return float(swe.sidtime(self.julian_day))

    def __str__(self) -> str:
        return self.dt.isoformat()

    def __repr__(self) -> str:
        return f"<Time JD={self.julian_day:.6f} DT={self.dt.isoformat()}>"
