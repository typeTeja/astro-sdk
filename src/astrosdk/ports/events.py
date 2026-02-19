from typing import Protocol, Optional, Dict
from astrosdk.core.time import Time

class EventProvider(Protocol):
    """
    Abstract interface for astronomical event search.
    """
    
    def find_next_solar_eclipse(self, start_time: Time) -> Optional[Time]:
        """Find next solar eclipse."""
        ...
        
    def find_next_lunar_eclipse(self, start_time: Time) -> Optional[Time]:
        """Find next lunar eclipse."""
        ...
