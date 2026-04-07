from ..core.constants import Planet, SiderealMode, ZodiacSign
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..schemas.events import IngressSchema, RetrogradeSchema
from .crossing_service import CrossingService


class EventsService:
    """
    Orchestration service for major planetary events and timeline generation.
    """

    def __init__(self, ephemeris: Ephemeris, crossing_service: CrossingService) -> None:
        self.eph = ephemeris
        self.crossing = crossing_service

    def get_sign_ingresses(
        self,
        start_time: Time,
        planet: Planet,
        count: int = 1,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
    ) -> list[IngressSchema]:
        """
        Find the next N sign ingresses for a given planet.
        """
        ingresses: list[IngressSchema] = []
        current_time = start_time

        for _ in range(count):
            try:
                # find_next_ingress returns (Time, SignNum)
                t, sign_num = self.crossing.find_next_ingress(
                    planet, current_time, sidereal_mode=sidereal_mode
                )

                # To get 'from_sign', calculate position slightly before ingress
                t_before = Time.from_julian_day(t.julian_day - 0.01)
                pos_before = self.eph.calculate_planet(t_before.julian_day, planet, sidereal=True)
                from_sign_id = int(pos_before["longitude"] / 30)

                ingresses.append(
                    IngressSchema(
                        planet=planet.name,
                        time=t.dt,
                        from_sign=ZodiacSign(from_sign_id).name,
                        to_sign=ZodiacSign(sign_num - 1).name,
                    )
                )

                # Advance search for next ingress
                current_time = Time.from_julian_day(t.julian_day + 1.0)
            except Exception:
                break  # Limit search if not found

        return ingresses

    def get_retrograde_stations(
        self, start_time: Time, planet: Planet, count: int = 1
    ) -> list[RetrogradeSchema]:
        """
        Find the next N retrograde/direct station points.
        """
        stations: list[RetrogradeSchema] = []
        current_jd = start_time.julian_day

        # Sun and Moon don't go retrograde
        if planet in [Planet.SUN, Planet.MOON]:
            return []

        for _ in range(count):
            # find_stationary_point(jd_start, planet, forward)
            stat_jd = self.eph.calculate_stationary_point(
                current_jd, planet, forward=True, max_days=365
            )

            if stat_jd:
                # Detect station type (Rx or Dir)
                # Check speed slightly after the station
                t_after = stat_jd + 0.1
                speed_after = self.eph.calculate_planet(t_after, planet)["speed_long"]

                stations.append(
                    RetrogradeSchema(
                        planet=planet.name,
                        time=Time.from_julian_day(stat_jd).dt,
                        station_type="RETROGRADE" if speed_after < 0 else "DIRECT",
                    )
                )

                # Advance search
                current_jd = stat_jd + 5.0  # Move past station
            else:
                break

        return stations
