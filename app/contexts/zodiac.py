from enum import StrEnum

from pydantic import BaseModel, Field

from ..core.constants import SiderealMode


class ZodiacType(StrEnum):
    SIDEREAL = "sidereal"
    TROPICAL = "tropical"


class ZodiacContext(BaseModel):
    """Zodiac and ayanamsa settings for a calculation."""

    zodiac: ZodiacType = Field(default=ZodiacType.SIDEREAL)
    sidereal_mode: SiderealMode | None = Field(default=SiderealMode.LAHIRI)

    @property
    def is_sidereal(self) -> bool:
        return self.zodiac == ZodiacType.SIDEREAL and self.sidereal_mode is not None
