from enum import StrEnum

from pydantic import BaseModel, Field


class CoordinateSystem(StrEnum):
    GEOCENTRIC = "geocentric"
    HELIOCENTRIC = "heliocentric"
    TOPOCENTRIC = "topocentric"


class CoordinateContext(BaseModel):
    """Coordinate system settings for a calculation."""

    system: CoordinateSystem = Field(default=CoordinateSystem.GEOCENTRIC)

    @property
    def is_heliocentric(self) -> bool:
        return self.system == CoordinateSystem.HELIOCENTRIC

    @property
    def is_topocentric(self) -> bool:
        return self.system == CoordinateSystem.TOPOCENTRIC
