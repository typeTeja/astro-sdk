from datetime import datetime, timedelta

from ..core.constants import Planet, SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.planet import PlanetPosition
from .natal_service import NatalService


from dataclasses import dataclass, field


@dataclass
class DashaPeriod:
    """Domain model for a Vimshottari dasha period (no Pydantic dependency)."""

    lord: str
    start_time: datetime
    end_time: datetime
    level: int
    sub_periods: list["DashaPeriod"] = field(default_factory=list)


class VedicService:
    """
    Service for calculating professional Vedic divisions and dasha systems.
    """

    DASHA_LORDS = [
        ("Ketu", 7),
        ("Venus", 20),
        ("Sun", 6),
        ("Moon", 10),
        ("Mars", 7),
        ("Rahu", 18),
        ("Jupiter", 16),
        ("Saturn", 19),
        ("Mercury", 17),
    ]

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris
        self.natal_service = NatalService(ephemeris)

    def calculate_varga_positions(
        self,
        time: Time,
        division: int,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
    ) -> list[PlanetPosition]:
        """
        Calculate planetary positions for divisional charts (Vargas).
        Returns domain PlanetPosition objects with the varga longitude.
        """
        planets = self.natal_service.calculate_positions(time, sidereal_mode)
        from ..domain.planet import PlanetPosition as PP
        from dataclasses import replace
        varga_planets: list[PlanetPosition] = []

        for p in planets:
            original_lon = p.longitude

            if division == 9:
                # Traditional Navamsa (D9) cycle
                sign_idx = int(original_lon / 30)
                cycle_starts = [0, 9, 6, 3]
                start_sign = cycle_starts[sign_idx % 4]

                nav_idx = int((original_lon % 30) / (30 / 9))
                v_sign = (start_sign + nav_idx) % 12
                v_deg = (original_lon % (30 / 9)) * 9
                v_lon = (v_sign * 30) + v_deg
            else:
                # Standard proportional multiplication for other Vargas
                v_lon = (original_lon * division) % 360

            # Return a new PlanetPosition frozen dataclass with the varga longitude
            varga_planets.append(
                PP(
                    planet=p.planet,
                    longitude=v_lon,
                    latitude=p.latitude,
                    distance=p.distance,
                    speed_long=p.speed_long,
                    speed_lat=p.speed_lat,
                    speed_dist=p.speed_dist,
                )
            )

        return varga_planets

    def calculate_dashas(
        self,
        natal_time: Time,
        cycles: int = 1,
        levels: int = 2,
        sidereal_mode: SiderealMode = SiderealMode.LAHIRI,
    ) -> list[DashaPeriod]:
        """
        Calculate Vimshottari Mahadasha and Antardasha periods.
        Returns domain DashaPeriod objects.
        """
        moon_pos = self.eph.calculate_planet(natal_time.julian_day, Planet.MOON, sidereal=True)
        moon_lon = moon_pos["longitude"]

        # 1. Start Nakshatra positioning
        nak_pos = moon_lon / (360 / 27)
        nak_idx = int(nak_pos)
        rem_nak = 1.0 - (nak_pos - nak_idx)

        start_lord_idx = nak_idx % 9
        mahadashas: list[DashaPeriod] = []
        current_time = natal_time.dt

        def add_years(dt: datetime, years: float) -> datetime:
            return dt + timedelta(days=years * 365.25)

        # Calculate Mahadashas (Level 1)
        lord_iter = start_lord_idx
        for i in range(cycles * 9):
            lord_name, duration_years = self.DASHA_LORDS[lord_iter % 9]

            if i == 0:
                # Partially spent the first dasha in life
                actual_duration = float(duration_years * rem_nak)
                start_dt = current_time
                end_dt = add_years(current_time, actual_duration)
            else:
                start_dt = current_time
                end_dt = add_years(current_time, float(duration_years))

            md = DashaPeriod(
                lord=lord_name,
                start_time=start_dt,
                end_time=end_dt,
                level=1,
                sub_periods=[],
            )

            # 2. Level 2 (Antardasha)
            if levels >= 2:
                md.sub_periods = self._calculate_antardashas(md, lord_iter % 9)

            mahadashas.append(md)
            current_time = end_dt
            lord_iter += 1

        return mahadashas

    def _calculate_antardashas(
        self, mahadasha: DashaPeriod, md_lord_idx: int
    ) -> list[DashaPeriod]:
        """
        Splits a Mahadasha into its 9 Antardashas.
        Returns domain DashaPeriod objects.
        """
        results: list[DashaPeriod] = []
        md_duration_days = (mahadasha.end_time - mahadasha.start_time).total_seconds() / (24 * 3600)

        current_start = mahadasha.start_time
        total_cycle_years = 120.0

        for i in range(9):
            ad_lord_idx = (md_lord_idx + i) % 9
            ad_lord_name, ad_lord_years = self.DASHA_LORDS[ad_lord_idx]

            proportion = ad_lord_years / total_cycle_years
            ad_duration_days = md_duration_days * proportion

            end_time = current_start + timedelta(days=ad_duration_days)

            results.append(
                DashaPeriod(
                    lord=ad_lord_name,
                    start_time=current_start,
                    end_time=end_time,
                    level=2,
                    sub_periods=[],
                )
            )
            current_start = end_time

        return results
