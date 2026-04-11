from ...contexts import CalculationContext


class AstronomyHorizonService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context

    def get_twilight(
        self,
        time: Time,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        twilight_type: str = "civil"
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
