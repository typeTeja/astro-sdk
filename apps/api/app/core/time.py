from datetime import UTC, datetime, timedelta
from typing import Self
from zoneinfo import ZoneInfo

import swisseph as swe

from app.core.errors import InvalidTimeError


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
        """Convert a UTC datetime to Julian Day using NASA JPLEPH / Swiss Ephemeris standard."""
        # Convert fractional seconds to match SwissEph format
        h_frac = dt.hour + dt.minute / 60.0 + dt.second / 3600.0 + dt.microsecond / 3.6e9
        
        # Returns (JD_ET, JD_UT) tuple, we want UT (0: ET, 1: UT)
        jd_arr = swe.utc_to_jd(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond / 1e6, swe.GREG_CAL)
        return float(jd_arr[1])

    @classmethod
    def from_julian_day(cls, jd: float) -> Self:
        """Create a Time object from a Julian Day (UT) using exact reverse mapping."""
        y, m, d, h_frac = swe.revjul(jd, swe.GREG_CAL)
        
        # h_frac represents the hour part. It can have fractional hours.
        # swe.utc_to_jd actually has an array output and its reverse is revjul.
        hour = int(h_frac)
        minute_frac = (h_frac - hour) * 60
        minute = int(minute_frac)
        second_frac = (minute_frac - minute) * 60
        second = int(second_frac)
        microsecond = int(round((second_frac - second) * 1e6))
        
        # Handle microsecond overflow rounding (e.g., 999999.something rolls over)
        if microsecond == 1000000:
            microsecond = 0
            second += 1
            if second == 60:
                second = 0
                minute += 1
                if minute == 60:
                    minute = 0
                    hour += 1
        
        dt = datetime(y, m, d, hour, minute, second, microsecond, tzinfo=UTC)
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
