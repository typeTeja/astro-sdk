from ...contexts import CalculationContext
from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.ephemeris_context import EphemerisContext
from ...core.time import Time
from ...domain.common.metadata import DomainMetadata
from ...domain.mundane.event import EventType, ExactAspectEvent


class ExactAspectService:
    """Native 2.0 service for detecting exact second of planetary aspects."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()

    def scan_aspects(
        self,
        p1: Planet,
        p2: Planet,
        target_angle: float,
        start_time: Time,
        end_time: Time,
        step_days: float = 0.5,
        tolerance: float = 1e-7
    ) -> list[ExactAspectEvent]:
        """Scan a window for the exact moment two planets reach a target angular separation."""
        
        events = []
        # Aspect scans are typically Tropical unless otherwise specified
        # but we follow context settings
        z_ctx = self.context.zodiac
        sid_mode = z_ctx.sidereal_mode
        is_sidereal = z_ctx.zodiac == "sidereal" or sid_mode is not None
        
        with EphemerisContext(sid_mode=sid_mode):
            current_jd = start_time.julian_day
            end_jd = end_time.julian_day
            
            def get_diff(jd: float) -> float:
                pos1 = self._ephemeris.calculate_planet(jd, p1, sidereal=is_sidereal)
                pos2 = self._ephemeris.calculate_planet(jd, p2, sidereal=is_sidereal)
                # Angular difference normalized to [-180, 180]
                diff = (pos1["longitude"] - pos2["longitude"]) % 360
                return (diff - target_angle + 180) % 360 - 180

            last_diff = get_diff(current_jd)
            
            while current_jd < end_jd:
                next_jd = min(current_jd + step_days, end_jd)
                current_diff = get_diff(next_jd)
                
                # Check for crossing (zero-crossing of the difference from target)
                if last_diff * current_diff < 0 and abs(last_diff - current_diff) < 180:
                    exact_jd = self._refine_aspect(p1, p2, target_angle, current_jd, next_jd, last_diff, is_sidereal, tolerance)
                    
                    events.append(
                        ExactAspectEvent(
                            type=EventType.ASPECT,
                            time=Time.from_julian_day(exact_jd).dt,
                            julian_day=exact_jd,
                            metadata=DomainMetadata(
                                capability="mundane.aspect",
                                maturity=self.context.feature.maturity.value,
                                fingerprint=f"v2-exact-aspect-{p1.name}-{p2.name}-{target_angle}"
                            ),
                            primary_planet=p1,
                            secondary_planet=p2,
                            aspect_type=f"ANGLE_{int(target_angle)}",
                            target_angle=target_angle
                        )
                    )
                
                last_diff = current_diff
                current_jd = next_jd
                
        return events

    def _refine_aspect(
        self,
        p1: Planet,
        p2: Planet,
        target_angle: float,
        jd1: float,
        jd2: float,
        d1: float,
        sidereal: bool,
        tolerance: float
    ) -> float:
        """Bisection refinement for aspect angular crossing."""
        low = jd1
        high = jd2
        
        def get_diff(jd: float) -> float:
            pos1 = self._ephemeris.calculate_planet(jd, p1, sidereal=sidereal)
            pos2 = self._ephemeris.calculate_planet(jd, p2, sidereal=sidereal)
            diff = (pos1["longitude"] - pos2["longitude"]) % 360
            return (diff - target_angle + 180) % 360 - 180

        for _ in range(35):
            mid = (low + high) / 2
            dm = get_diff(mid)
            
            if (d1 > 0) == (dm > 0):
                low = mid
            else:
                high = mid
                
            if abs(high - low) < tolerance:
                break
        return (low + high) / 2
