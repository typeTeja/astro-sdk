from ...contexts import CalculationContext
from ...core.ephemeris import Ephemeris
from ...core.time import Time
from ...domain.common.metadata import DomainMetadata
from ...domain.mundane.event import EclipseEvent, EventType


class EclipseService:
    """Native 2.0 service for detecting Solar and Lunar eclipses."""

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._ephemeris = ephemeris or Ephemeris()

    def find_next_solar_eclipse(self, start_time: Time) -> EclipseEvent:
        """Find the next solar eclipse globally."""
        res = self._ephemeris.search_solar_eclipse(start_time.julian_day)
        return EclipseEvent(
            type=EventType.ECLIPSE,
            time=Time.from_julian_day(res["peak_jd"]).dt,
            julian_day=res["peak_jd"],
            metadata=DomainMetadata(
                capability="mundane.eclipse",
                maturity=self.context.feature.maturity.value,
                fingerprint=f"v2-solar-eclipse-{res['peak_jd']:.4f}"
            ),
            eclipse_type="SOLAR",
            magnitude=res["magnitude"],
            is_total=res["magnitude"] >= 1.0,
            is_annular=False, # EPHE logic needs refinement for annular but stubs as False for parity
            peak_jd=res["peak_jd"]
        )

    def find_next_lunar_eclipse(self, start_time: Time) -> EclipseEvent:
        """Find the next lunar eclipse."""
        res = self._ephemeris.search_lunar_eclipse(start_time.julian_day)
        return EclipseEvent(
            type=EventType.ECLIPSE,
            time=Time.from_julian_day(res["peak_jd"]).dt,
            julian_day=res["peak_jd"],
            metadata=DomainMetadata(
                capability="mundane.eclipse",
                maturity=self.context.feature.maturity.value,
                fingerprint=f"v2-lunar-eclipse-{res['peak_jd']:.4f}"
            ),
            eclipse_type="LUNAR",
            magnitude=res["magnitude"],
            is_total=res["magnitude"] >= 1.0,
            is_annular=False,
            peak_jd=res["peak_jd"]
        )
