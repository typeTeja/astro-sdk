from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import math
from .exceptions import InvalidTimeError

class Time:
    """
    Deterministic time representation (UTC).
    Pure Value Object. No external dependencies.
    """
    def __init__(self, dt: datetime):
        if dt.tzinfo is None:
            raise InvalidTimeError("Naive datetime not allowed. Must be timezone-aware.")
        self._dt = dt.astimezone(timezone.utc)

    @property
    def dt(self) -> datetime:
        """Returns the underlying UTC datetime."""
        return self._dt

    @classmethod
    def from_string(cls, date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S", tz: str = "UTC") -> 'Time':
        try:
            dt = datetime.strptime(date_str, format_str)
            dt = dt.replace(tzinfo=ZoneInfo(tz))
            return cls(dt)
        except ValueError as e:
            raise InvalidTimeError(f"Invalid time format: {str(e)}")

    @property
    def julian_day(self) -> float:
        """
        Calculates Julian Day Number (UT) using pure Python.
        Algorithm: Meeus (1998)
        """
        year = self._dt.year
        month = self._dt.month
        day = self._dt.day
        
        # Adjust for Jan/Feb
        if month <= 2:
            year -= 1
            month += 12
            
        # Calculate time fraction
        # (microsecond precision)
        fraction = (self._dt.hour + self._dt.minute / 60.0 + self._dt.second / 3600.0 + self._dt.microsecond / 3600000000.0) / 24.0
        
        # Gregorian Calendar adjustment
        # AstroSDK assumes Gregorian for all supported dates (standard modern astrology)
        A = math.floor(year / 100)
        B = 2 - A + math.floor(A / 4)
        
        jd_midnight = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
        
        return jd_midnight + fraction

    def __repr__(self) -> str:
        return f"Time(utc={self._dt.isoformat()})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Time):
            return self._dt == other._dt
        return False

    def __hash__(self) -> int:
        return hash(self._dt)
