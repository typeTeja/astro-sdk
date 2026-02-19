from astrosdk.core.constants import Planet
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class CombustionState(str, Enum):
    """State of planetary combustion relative to the Sun."""
    COMBUST = "combust"           # Within combustion orb
    UNDER_BEAMS = "under_beams"   # Within 17 deg
    CAZIMI = "cazimi"             # Exact conjunction
    FREE = "free"                 # Outside solar influence

class CombustionResult(BaseModel):
    """Result of combustion analysis."""
    model_config = ConfigDict(frozen=True)
    
    state: CombustionState
    orb_from_sun: float = Field(ge=0.0, description="Angular distance from Sun")
    threshold_used: float
    is_cazimi: bool

# Default combustion orbs (moved to config in Phase 3, keeping here for now as default)
# v2.md says "Externalize configurable rules".
# But for Phase 1, I can keep them as constants here or in `config.default_rules`.
# Pass them as arguments is better.

CAZIMI_ORB = 0.283 # 17 arcminutes

def calculate_combustion(
    planet_longitude: float,
    sun_longitude: float,
    threshold: float
) -> CombustionResult:
    """
    Pure function to calculate combustion.
    Does NOT depend on Planet enum for defaults (must be passed).
    """
    diff = abs(planet_longitude - sun_longitude)
    if diff > 180:
        diff = 360 - diff
    
    orb = diff
    
    if orb <= CAZIMI_ORB:
        return CombustionResult(
            state=CombustionState.CAZIMI,
            orb_from_sun=orb,
            threshold_used=threshold,
            is_cazimi=True
        )
        
    if orb <= threshold:
        return CombustionResult(
            state=CombustionState.COMBUST,
            orb_from_sun=orb,
            threshold_used=threshold,
            is_cazimi=False
        )
        
    if orb <= 17.0:
        return CombustionResult(
            state=CombustionState.UNDER_BEAMS,
            orb_from_sun=orb,
            threshold_used=threshold,
            is_cazimi=False
        )
        
    return CombustionResult(
        state=CombustionState.FREE,
        orb_from_sun=orb,
        threshold_used=threshold,
        is_cazimi=False
    )
