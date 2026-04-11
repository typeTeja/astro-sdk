from pydantic import BaseModel, Field

from .coordinate import CoordinateContext
from .feature import FeatureContext
from .house import HouseContext
from .observer import ObserverContext
from .time import TimeContext
from .zodiac import ZodiacContext


class CalculationContext(BaseModel):
    """Top-level calculation context for AstroSDK 2.0 services."""

    zodiac: ZodiacContext = Field(default_factory=ZodiacContext)
    coordinate: CoordinateContext = Field(default_factory=CoordinateContext)
    house: HouseContext = Field(default_factory=HouseContext)
    time: TimeContext = Field(default_factory=TimeContext)
    observer: ObserverContext | None = Field(default=None)
    feature: FeatureContext = Field(
        default_factory=lambda: FeatureContext(capability="core.generic")
    )

    def fingerprint_payload(self) -> dict[str, object]:
        """Return a stable payload for reproducibility metadata."""

        return self.model_dump(mode="json", exclude_none=True)

    @property
    def fingerprint(self) -> str:
        """Calculate the deterministic fingerprint for this context."""
        from ..core.fingerprint import calculation_fingerprint
        return calculation_fingerprint(self.fingerprint_payload())
