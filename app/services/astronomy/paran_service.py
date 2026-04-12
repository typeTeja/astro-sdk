from typing import Any
from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata


class AstronomyParanService:
    """
    Native 2.0 service for calculating Parans (simultaneous horizon/meridian events).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def find_parans(
        self,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        orb_minutes: float = 5.0
    ) -> list[dict[str, Any]]:
        """
        Find all parans occurring on the calendar day of the given time using the 2.0 context.
        """
        import datetime
        from app.core.ephemeris_context import EphemerisContext
        
        midnight = Time(
            datetime.datetime(time.dt.year, time.dt.month, time.dt.day, tzinfo=datetime.UTC)
        )
        jd_midnight = midnight.julian_day

        events: list[dict[str, Any]] = []
        # Check major planets
        planets = [p for p in Planet if p <= Planet.PLUTO or p == Planet.MOON]

        with EphemerisContext(topo=(lon, lat, altitude)):
            for p in planets:
                # Rise
                r = self._eph.calculate_rise_set(jd_midnight, p, lat, lon, altitude, is_rise=True)
                if r:
                    events.append({"planet": p, "type": "RISE", "jd": r})

                # Set
                s = self._eph.calculate_rise_set(jd_midnight, p, lat, lon, altitude, is_rise=False)
                if s:
                    events.append({"planet": p, "type": "SET", "jd": s})

                # Upper Transit (MC)
                t = self._eph.calculate_transit(jd_midnight, p, lat, lon, altitude)
                if t:
                    events.append({"planet": p, "type": "TRANSIT", "jd": t})

        # Compare pairs for simultaneity
        results = []
        orb_jd = orb_minutes / (24.0 * 60.0)

        for i in range(len(events)):
            for j in range(i + 1, len(events)):
                e1, e2 = events[i], events[j]
                if abs(float(e1["jd"]) - float(e2["jd"])) <= orb_jd:
                    results.append({
                        "p1": e1["planet"].name,
                        "type1": e1["type"],
                        "p2": e2["planet"].name,
                        "type2": e2["type"],
                        "time": Time.from_julian_day((float(e1["jd"]) + float(e2["jd"])) / 2.0).dt,
                        "orb_minutes": abs(float(e1["jd"]) - float(e2["jd"])) * 1440.0,
                        "metadata": DomainMetadata(
                            capability="astronomy.paran",
                            maturity=self.context.feature.maturity.value,
                            fingerprint=self.context.fingerprint
                        )
                    })
        return results
