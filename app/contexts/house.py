from pydantic import BaseModel, Field

from app.core.constants import HouseSystem


class HouseContext(BaseModel):
    """House calculation settings."""

    system: HouseSystem = Field(default=HouseSystem.PLACIDUS)
