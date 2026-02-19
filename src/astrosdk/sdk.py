from typing import Optional
from .config.astro_config import AstroConfig
from .infrastructure.swisseph import SwissEphemerisEngine, SwissEphemerisAdapter
from .application.natal_service import NatalService
from .application.aspect_service import AspectService

class AstroSDK:
    """
    Composition Root.
    Wires the hexagonal architecture together.
    """
    
    def __init__(self, config: Optional[AstroConfig] = None):
        self.config = config or AstroConfig()
        
        # Infrastructure
        self._engine = SwissEphemerisEngine(ephe_path=self.config.ephemeris_path or None)
        self._adapter = SwissEphemerisAdapter(self._engine)
        
        # Application Services
        self.natal = NatalService(self._adapter, self._adapter, self.config)
        self.aspects = AspectService(self.config)
        # Add events, acceleration, etc.
        
    def create_natal_chart(self, *args, **kwargs):
        """Facade method for convenience."""
        return self.natal.calculate_natal_chart(*args, **kwargs)
        
def create_sdk(config: Optional[AstroConfig] = None) -> AstroSDK:
    """Factory function."""
    return AstroSDK(config)
