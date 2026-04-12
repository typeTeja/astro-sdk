from pydantic import BaseModel, Field

from app.contexts.coordinate import CoordinateContext
from app.contexts.feature import FeatureContext
from app.contexts.house import HouseContext
from app.contexts.observer import ObserverContext
from app.contexts.time import TimeContext
from app.contexts.zodiac import ZodiacContext


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

    def apply_settings(self, settings: "ChartSettings") -> None:
        """
        Map a resolved ChartSettings object onto the internal contexts.
        """
        from app.contexts.coordinate import CoordinateSystem
        from app.contexts.zodiac import ZodiacType

        # 1. Zodiac
        self.zodiac.zodiac = ZodiacType(settings.zodiac)
        self.zodiac.sidereal_mode = settings.sidereal_mode

        # 2. Coordinate System
        self.coordinate.system = CoordinateSystem(settings.coordinate_system)

        # 3. House System
        if settings.house_system:
            self.house.system = settings.house_system

        # 4. Feature Context (Optional updates based on settings)
        if settings.aspect_system:
             self.feature.capability = f"core.{settings.aspect_system}"


    def fingerprint_payload(self) -> dict[str, object]:
        """Return a stable payload for reproducibility metadata."""

        return self.model_dump(mode="json", exclude_none=True)

    @property
    def fingerprint(self) -> str:
        """Calculate the deterministic fingerprint for this context."""
        from app.core.fingerprint import calculation_fingerprint
        return calculation_fingerprint(self.fingerprint_payload())
