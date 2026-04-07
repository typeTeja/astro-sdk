from ..core.constants import Planet, SiderealMode, ZodiacSign
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.events import PlanetaryEvent
from .crossing_service import CrossingService


class EventsService:
    """
    Orchestration service for major planetary events and timeline generation.
    Returns domain PlanetaryEvent objects; schema conversion is the API layer's responsibility.
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
    ) -> list[PlanetaryEvent]:
        """
        Find the next N sign ingresses for a given planet.
        Returns domain PlanetaryEvent objects with event_type='INGRESS'.
        """
        results: list[PlanetaryEvent] = []
        current_time = start_time

        for _ in range(count):
            try:
                # find_next_ingress returns (Time, SignNum)
                t, sign_num = self.crossing.find_next_ingress(
                    planet, current_time, sidereal_mode=sidereal_mode
                )

                # Determine the sign we are leaving
                t_before = Time.from_julian_day(t.julian_day - 0.01)
                pos_before = self.eph.calculate_planet(t_before.julian_day, planet, sidereal=True)
                from_sign_id = int(pos_before["longitude"] / 30)

                results.append(
                    PlanetaryEvent(
                        planet=planet,
                        event_type="INGRESS",
                        time=t.dt,
                        sign_id=sign_num,
                        is_retrograde=False,
                        from_sign=ZodiacSign(from_sign_id).name,
                        to_sign=ZodiacSign(sign_num - 1).name,
                    )
                )

                # Advance the search window past this ingress
                current_time = Time.from_julian_day(t.julian_day + 1.0)
            except Exception:
                break

        return results

    def get_retrograde_stations(
        self, start_time: Time, planet: Planet, count: int = 1
    ) -> list[PlanetaryEvent]:
        """
        Find the next N retrograde/direct station points.
        Returns domain PlanetaryEvent objects with event_type='STATION'.
        """
        stations: list[PlanetaryEvent] = []
        current_jd = start_time.julian_day

        if planet in [Planet.SUN, Planet.MOON]:
            return []

        for _ in range(count):
            stat_jd = self.eph.calculate_stationary_point(
                current_jd, planet, forward=True, max_days=365
            )

            if stat_jd:
                t_after = stat_jd + 0.1
                speed_after = self.eph.calculate_planet(t_after, planet)["speed_long"]
                is_rx = speed_after < 0

                stations.append(
                    PlanetaryEvent(
                        planet=planet,
                        event_type="STATION",
                        time=Time.from_julian_day(stat_jd).dt,
                        is_retrograde=is_rx,
                        station_type="RETROGRADE" if is_rx else "DIRECT",
                    )
                )
                current_jd = stat_jd + 5.0
            else:
                break

        return stations
