from pydantic import BaseModel, Field, ConfigDict
from ..core.constants import Planet

class Aspect(BaseModel):
    """Planetary aspect with orb and application status."""
    model_config = ConfigDict(frozen=True)
    
    p1: Planet = Field(description="First planet")
    p2: Planet = Field(description="Second planet")
    angle: float = Field(ge=0.0, lt=360.0, description="Exact aspect angle")
    orb: float = Field(ge=0.0, description="Orb from exactitude (absolute value)")
    type: str = Field(description="Aspect type (CONJUNCTION, SQUARE, etc.)")
    applying: bool = Field(description="True if aspect is applying (getting tighter)")
