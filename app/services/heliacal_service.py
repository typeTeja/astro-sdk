from typing import Any

from ..core.constants import Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time


class HeliacalService:
    """
    Service for specialized celestial events like heliacal rising/setting
    and planetary stations.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris

    def calculate_heliacal_rising(
        self,
        planet: Planet,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        star_name: str = "",
    ) -> Time | None:
        """Calculate next heliacal rising after given time."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day,
            planet,
            lat,
            lon,
            altitude,
            event_type=1,
            star_name=star_name,
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None

    def calculate_heliacal_setting(
        self,
        planet: Planet,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        star_name: str = "",
    ) -> Time | None:
        """Calculate next heliacal setting after given time."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day,
            planet,
            lat,
            lon,
            altitude,
            event_type=2,
            star_name=star_name,
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None

    def find_all_stations(
        self, planet: Planet, year: int, forward: bool = True
    ) -> list[dict[str, Any]]:
        """
        Find all stationary points (Retrograde/Direct) for a planet in a given year.
        """
        results: list[dict[str, Any]] = []
        import datetime

        current_jd = Time(datetime.datetime(year, 1, 1, tzinfo=datetime.UTC)).julian_day
        end_jd = Time(datetime.datetime(year, 12, 31, 23, 59, tzinfo=datetime.UTC)).julian_day

        while current_jd < end_jd:
            station_jd = self.eph.calculate_stationary_point(
                current_jd, planet, forward=True, max_days=365
            )
            if station_jd is None or station_jd > end_jd:
                break

            speed_before = self.eph.calculate_planet(station_jd - 0.01, planet)["speed_long"]
            s_type = "Retrograde Station" if speed_before > 0 else "Direct Station"

            results.append(
                {
                    "time": Time.from_julian_day(station_jd),
                    "type": s_type,
                    "jd": station_jd,
                }
            )

            current_jd = station_jd + 5.0

        return results

    def calculate_acronychal_rising(
        self,
        planet: Planet,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        star_name: str = "",
    ) -> Time | None:
        """Calculate next acronychal rising (rising at sunset)."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day,
            planet,
            lat,
            lon,
            altitude,
            event_type=5,
            star_name=star_name,
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None

    def calculate_cosmical_setting(
        self,
        planet: Planet,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        star_name: str = "",
    ) -> Time | None:
        """Calculate next cosmical setting (setting at sunrise)."""
        res = self.eph.calculate_heliacal_event(
            time.julian_day,
            planet,
            lat,
            lon,
            altitude,
            event_type=6,
            star_name=star_name,
        )
        return Time.from_julian_day(res["event_jd"]) if "event_jd" in res else None
