from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.ephemeris_context import EphemerisContext
from app.core.time import Time


class AstronomyHorizonService:
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def get_horizon_event(
        self,
        planet: Planet,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        is_rise: bool = True,
    ) -> Time | None:
        """Calculate the next rise or set time for a planet."""
        with EphemerisContext(topo=(lon, lat, altitude)):
            event_jd = self._eph.calculate_rise_set(
                time.julian_day, planet, lat, lon, altitude, is_rise=is_rise
            )
            return Time.from_julian_day(event_jd) if event_jd else None

    def get_transit(
        self,
        planet: Planet,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
    ) -> Time | None:
        """Calculate the next meridian transit (culmination) for a planet."""
        with EphemerisContext(topo=(lon, lat, altitude)):
            transit_jd = self._eph.calculate_transit(time.julian_day, planet, lat, lon, altitude)
            return Time.from_julian_day(transit_jd) if transit_jd else None

    def get_twilight(
        self,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        twilight_type: str = "civil",
    ) -> dict[str, Time | None]:
        """
        Calculate dawn and dusk for different twilight categories.
        """
        import swisseph as swe

        types = {
            "civil": swe.BIT_CIVIL_TWILIGHT,
            "nautical": swe.BIT_NAUTIC_TWILIGHT,
            "astronomical": swe.BIT_ASTRO_TWILIGHT,
        }

        if twilight_type not in types:
            raise ValueError(f"Unknown twilight type: {twilight_type}")

        bit = types[twilight_type]
        with EphemerisContext(topo=(lon, lat, altitude)):
            dawn_jd = self._eph.calculate_rise_set(
                time.julian_day, Planet.SUN, lat, lon, altitude, is_rise=True, rsmi_extra=bit
            )
            dusk_jd = self._eph.calculate_rise_set(
                time.julian_day, Planet.SUN, lat, lon, altitude, is_rise=False, rsmi_extra=bit
            )

            return {
                "dawn": Time.from_julian_day(dawn_jd) if dawn_jd else None,
                "dusk": Time.from_julian_day(dusk_jd) if dusk_jd else None,
            }
