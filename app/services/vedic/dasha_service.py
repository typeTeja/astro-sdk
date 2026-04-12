from datetime import timedelta

from app.contexts import CalculationContext
from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.ephemeris_context import EphemerisContext
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata
from app.domain.vedic.dasha import DashaPeriod


class VedicDashaService:
    """
    Service for calculating Vimshottari Dashas.
    Uses the 2.0 context model for deterministic sidereal calculations.
    """

    # 120-year cycle sequence
    DASHA_SEQUENCE = [
        ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10),
        ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19),
        ("Mercury", 17)
    ]

    def __init__(self, context: CalculationContext) -> None:
        self.context = context
        self._eph = Ephemeris()

    def calculate_mahadashas(self, time: Time) -> list[DashaPeriod]:
        """
        Calculate the Mahadasha sequence for a given birth time.
        """
        sid_mode = self.context.zodiac.sidereal_mode or SiderealMode.LAHIRI

        with EphemerisContext(sid_mode=sid_mode):
            # 1. Get Moon Sidereal Longitude
            moon_pos = self._eph.calculate_planet(time.julian_day, Planet.MOON, sidereal=True)
            moon_lon = moon_pos["longitude"]

            # 2. Identify Nakshatra and Starting Dasha
            # Each nakshatra is 13°20' (13.3333 degrees)
            nak_width = 360 / 27
            nak_idx = int(moon_lon / nak_width)

            # Starting lord index (Ketu is lord of 1st, 10th, 19th nakshatra)
            lord_idx = nak_idx % 9

            # Progress into the current nakshatra
            nak_start_lon = nak_idx * nak_width
            progress = (moon_lon - nak_start_lon) / nak_width

            # 3. Calculate First Dasha end time
            current_lord_name, total_years = self.DASHA_SEQUENCE[lord_idx]


            # Create the sequence (calculate for 120 years from birth or at least full cycle)
            results = []

            # Note: Simplistic conversion (365.25 days per year)
            current_start = time.dt
            # The first dasha started total_years * progress ago
            elapsed_years = total_years * progress
            first_dasha_start = current_start - timedelta(days=elapsed_years * 365.25)


            # Metadata
            meta = DomainMetadata(
                capability="vedic.dashas",
                maturity=self.context.feature.maturity.value,
                fingerprint=self.context.fingerprint
            )

            # We start from the current lord and go through the cycle
            temp_start = first_dasha_start
            for i in range(9):
                seq_idx = (lord_idx + i) % 9
                name, years = self.DASHA_SEQUENCE[seq_idx]

                period_end = temp_start + timedelta(days=years * 365.25)

                results.append(DashaPeriod(
                    lord=name,
                    start=temp_start,
                    end=period_end,
                    level=1, # Mahadasha
                    metadata=meta
                ) )

                temp_start = period_end

            return results
