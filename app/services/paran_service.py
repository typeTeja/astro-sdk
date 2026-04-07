from typing import Any

from ..core.constants import Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time


class ParanService:
    """
    Service for calculating Parans (simultaneous horizon/meridian events).
    A Paran occurs when two bodies hit any of the four angles at the same time.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris

    def find_parans(
        self,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        orb_minutes: float = 5.0,
    ) -> list[dict[str, Any]]:
        """
        Find all parans occurring on the calendar day of the given time.
        """
        import datetime

        midnight = Time(
            datetime.datetime(time.dt.year, time.dt.month, time.dt.day, tzinfo=datetime.UTC)
        )
        jd = midnight.julian_day

        events: list[dict[str, Any]] = []
        planets_to_check = [p for p in Planet if p <= Planet.PLUTO or p == Planet.MOON]

        for p in planets_to_check:
            # Rise
            r = self.eph.calculate_rise_set(jd, p, lat, lon, altitude, is_rise=True)
            if r:
                events.append({"planet": p, "type": "Rise", "jd": r})

            # Set
            s = self.eph.calculate_rise_set(jd, p, lat, lon, altitude, is_rise=False)
            if s:
                events.append({"planet": p, "type": "Set", "jd": s})

            # Transit (Upper)
            t = self.eph.calculate_transit(jd, p, lat, lon, altitude)
            if t:
                events.append({"planet": p, "type": "Transit", "jd": t})

            import swisseph as swe

            # IC (Lower Transit)
            ic = self.eph.calculate_rise_set(
                jd, p, lat, lon, altitude, rsmi_extra=swe.CALC_ITRANSIT
            )
            if ic:
                events.append({"planet": p, "type": "IC", "jd": ic})

        # 2. Compare all pairs
        results: list[dict[str, Any]] = []
        orb_jd = orb_minutes / (24.0 * 60.0)

        for i in range(len(events)):
            for j in range(i + 1, len(events)):
                e1 = events[i]
                e2 = events[j]

                # e1["jd"] is Any, but Mypy should handle the operator if it's not object
                if abs(float(e1["jd"]) - float(e2["jd"])) <= orb_jd:
                    results.append(
                        {
                            "p1": e1["planet"],
                            "type1": e1["type"],
                            "p2": e2["planet"],
                            "type2": e2["type"],
                            "time": Time.from_julian_day((float(e1["jd"]) + float(e2["jd"])) / 2.0),
                            "orb_minutes": abs(float(e1["jd"]) - float(e2["jd"])) * 24.0 * 60.0,
                        }
                    )

        return results
