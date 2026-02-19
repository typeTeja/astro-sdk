from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import swisseph as swe
from .errors import InvalidTimeError, InvalidTimeStandardError
from .ephemeris import _SWISS_LOCK, DEFAULT_EPHE_FLAG

class Time:
    """
    Deterministic time representation.
    Always UTC.
    """
    def __init__(self, dt: datetime):
        if dt.tzinfo is None:
            raise InvalidTimeError("Naive datetime not allowed. Must be timezone-aware.")
        self._dt = dt.astimezone(timezone.utc)

    @property
    def dt(self) -> datetime:
        return self._dt

    @property
    def julian_day(self) -> float:
        """
        Returns Julian Day in UT.
        """
        return swe.julday(
            self._dt.year, 
            self._dt.month, 
            self._dt.day, 
            self._dt.hour + self._dt.minute / 60.0 + self._dt.second / 3600.0 + self._dt.microsecond / 3600000000.0
        )

    @classmethod
    def from_julian_day(cls, jd: float) -> 'Time':
        """
        Create a Time object from a Julian Day (UT).
        """
        year, month, day, hour_float = swe.revjul(jd)
        # Use timedelta to safely add fractional hours to start of day
        base_dt = datetime(year, month, day, tzinfo=timezone.utc)
        dt = base_dt + timedelta(hours=hour_float)
        return cls(dt)

    @property
    def delta_t(self) -> float:
        """
        Returns Delta-T in days using the high-precision deltat_ex.
        """
        with _SWISS_LOCK:
            # swe.deltat_ex returns deltat_days as a float
            return swe.deltat_ex(self.julian_day, DEFAULT_EPHE_FLAG)

    @property
    def jd_et(self) -> float:
        """
        Returns Julian Day in ET (Ephemeris Time).
        """
        return self.julian_day + self.delta_t

    @property
    def sidereal_time(self) -> float:
        """
        Returns Greenwich Mean Sidereal Time in hours.
        """
        with _SWISS_LOCK:
            return swe.sidtime(self.julian_day)

    @classmethod
    def from_string(cls, date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S", tz: str = "UTC") -> 'Time':
        try:
            dt = datetime.strptime(date_str, format_str)
            dt = dt.replace(tzinfo=ZoneInfo(tz))
            return cls(dt)
        except ValueError as e:
            raise InvalidTimeError(f"Invalid time format: {str(e)}")
