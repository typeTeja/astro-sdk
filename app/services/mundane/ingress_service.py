from app.contexts import CalculationContext
from app.core.constants import ALLOWED_PLANETS, Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata
from app.domain.mundane.ingress import MundaneIngress


class MundaneIngressService:
    """
    Service for detecting planetary sign ingresses (entering a new sign).
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def scan_ingresses(self, planet: Planet, start_time: Time, end_time: Time) -> list[MundaneIngress]:
        """
        Scans for sign crossings for a planet between two dates.
        """
        if planet not in ALLOWED_PLANETS:
            return []

        events: list[MundaneIngress] = []
        current_jd = start_time.julian_day
        end_jd = end_time.julian_day

        # Step value in days (approx 10 steps per sign duration at max speed)
        # Moon: ~2.5 days/sign -> 0.25d steps
        # Sun: 30 days/sign -> 3d steps
        step = 0.25 if planet == Planet.MOON else 1.0

        while current_jd < end_jd:
            pos1 = self._eph.calculate_planet(current_jd, planet)
            pos2 = self._eph.calculate_planet(min(current_jd + step, end_jd), planet)

            s1 = int(pos1["longitude"] / 30.0)
            s2 = int(pos2["longitude"] / 30.0)

            if s1 != s2:
                # Sign boundary crossing detected. Refine with bisection.
                low = current_jd
                high = current_jd + step
                for _ in range(20):
                    mid = (low + high) / 2.0
                    pm = self._eph.calculate_planet(mid, planet)
                    sm = int(pm["longitude"] / 30.0)
                    if sm == s1:
                        low = mid
                    else:
                        high = mid

                final_jd = high
                sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
                events.append(
                    MundaneIngress(
                        planet=planet,
                        time=Time.from_julian_day(final_jd).dt,
                        from_sign=sign_names[s1 % 12],
                        to_sign=sign_names[s2 % 12],
                        metadata=DomainMetadata(
                            capability="mundane.ingresses",
                            maturity=self.context.feature.maturity.value,
                            fingerprint=self.context.fingerprint
                        )
                    )
                )
                current_jd = final_jd + 0.1 # Escape
            else:
                current_jd += step

        return events
