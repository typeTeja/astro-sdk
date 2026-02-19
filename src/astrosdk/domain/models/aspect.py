from pydantic import BaseModel, Field, ConfigDict
from astrosdk.core.constants import Planet

class Aspect(BaseModel):
    """Planetary aspect with orb and application status."""
    model_config = ConfigDict(frozen=True)
    
    p1: Planet
    p2: Planet
    angle: float
    orb: float
    type: str
    applying: bool
