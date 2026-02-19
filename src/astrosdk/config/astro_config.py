from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any
from .default_rules import DEFAULT_COMBUSTION_ORBS, DEFAULT_ASPECT_ORBS, WESTERN_DIGNITY_RULES

class AstroConfig(BaseModel):
    """
    Immutable configuration for the SDK.
    Passing a different config enables 'multi-tenancy' or research variations
    without global state mutation.
    """
    model_config = ConfigDict(frozen=True)
    
    ephemeris_path: str = Field(default="") # Empty string = use default
    combustion_orbs: Dict[Any, float] = Field(default=DEFAULT_COMBUSTION_ORBS)
    aspect_orbs: Dict[str, float] = Field(default=DEFAULT_ASPECT_ORBS)
    dignity_rules: Dict[Any, Any] = Field(default=WESTERN_DIGNITY_RULES)
