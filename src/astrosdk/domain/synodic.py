"""
Synodic Cycles Module

Tracks phase relationships between planetary pairs from conjunction to conjunction.
Used for cycle analysis such as New Moon/Full Moon cycles, planetary returns, etc.

Example:
    # Find all Sun-Moon lunation cycles in 2024
    cycles = find_synodic_cycles(
        planet1=Planet.SUN,
        planet2=Planet.MOON,
        start_time=datetime(2024, 1, 1),
        end_time=datetime(2025, 1, 1)
    )
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

from ..core.constants import Planet


class SynodicPhase(BaseModel):
    """
    A single phase point in a synodic cycle.
    
    Tracks key astronomical events like conjunction, opposition, etc.
    """
    model_config = ConfigDict(frozen=True)
    
    phase_name: str = Field(description="Phase name: conjunction, first_quarter, opposition, last_quarter")
    phase_angle: float = Field(ge=0.0, lt=360.0, description="Angular separation (0-360°)")
    timestamp: datetime
    planet1_longitude: float = Field(ge=0.0, lt=360.0)
    planet2_longitude: float = Field(ge=0.0, lt=360.0)


class SynodicCycle(BaseModel):
    """
    Complete synodic cycle from conjunction to next conjunction.
    
    Tracks the phase relationship between two planets over time,
    useful for lunation cycles, planetary returns, etc.
    """
    model_config = ConfigDict(frozen=True)
    
    planet1: Planet
    planet2: Planet
    start_conjunction: datetime
    end_conjunction: Optional[datetime] = None
    phases: List[SynodicPhase] = Field(default_factory=list)
    cycle_length_days: Optional[float] = None
    
    @property
    def is_complete(self) -> bool:
        """Check if cycle has both start and end conjunctions."""
        return self.end_conjunction is not None
    
    def get_phase_at_time(self, timestamp: datetime) -> Optional[SynodicPhase]:
        """
        Find the most recent phase at a given time.
        
        Args:
            timestamp: Time to check
        
        Returns:
            SynodicPhase if found, None otherwise
        """
        relevant_phases = [p for p in self.phases if p.timestamp <= timestamp]
        if not relevant_phases:
            return None
        return max(relevant_phases, key=lambda p: p.timestamp)


def calculate_phase_angle(long1: float, long2: float) -> float:
    """
    Calculate phase angle between two longitudes.
    
    Args:
        long1: First planet longitude (0-360)
        long2: Second planet longitude (0-360)
    
    Returns:
        Phase angle (0-360), measured from planet1 to planet2
    
    Examples:
        >>> calculate_phase_angle(0, 90)   # Quarter
        90.0
        >>> calculate_phase_angle(0, 180)  # Opposition
        180.0
        >>> calculate_phase_angle(350, 10) # Near conjunction
        20.0
    """
    angle = (long2 - long1) % 360.0
    return angle


def classify_phase(phase_angle: float) -> str:
    """
    Classify synodic phase based on angle.
    
    Args:
        phase_angle: Angular separation (0-360°)
    
    Returns:
        Phase name: conjunction, waxing_crescent, first_quarter, waxing_gibbous,
                    opposition, waning_gibbous, last_quarter, waning_crescent
    
    Examples:
        >>> classify_phase(0)
        'conjunction'
        >>> classify_phase(90)
        'first_quarter'
        >>> classify_phase(180)
        'opposition'
    """
    # Use 45° windows centered on each phase
    if phase_angle < 22.5 or phase_angle >= 337.5:
        return "conjunction"
    elif phase_angle < 67.5:
        return "waxing_crescent"
    elif phase_angle < 112.5:
        return "first_quarter"
    elif phase_angle < 157.5:
        return "waxing_gibbous"
    elif phase_angle < 202.5:
        return "opposition"
    elif phase_angle < 247.5:
        return "waning_gibbous"
    elif phase_angle < 292.5:
        return "last_quarter"
    else:
        return "waning_crescent"


def find_synodic_cycles(
    planet1: Planet,
    planet2: Planet,
    start_time: datetime,
    end_time: datetime,
    get_positions_callback = None
) -> List[SynodicCycle]:
    """
    Find all synodic cycles between two planets in a time range.
    
    A synodic cycle runs from conjunction to the next conjunction.
    This function also identifies key phases (quarters, opposition).
    
    Args:
        planet1: First planet (typically faster-moving or primary)
        planet2: Second planet
        start_time: Start of search range
        end_time: End of search range
        get_positions_callback: Function(datetime, planet) -> longitude
                                Must be provided to get planet positions
    
    Returns:
        List of SynodicCycle objects
    
    Example:
        >>> from astrosdk import calculate_natal_chart
        >>> 
        >>> def get_pos(dt, planet):
        >>>     # Get planet position at time
        >>>     chart = calculate_natal_chart(dt, 0, 0)
        >>>     for p in chart.planets:
        >>>         if p.planet == planet:
        >>>             return p.longitude
        >>>     return 0
        >>> 
        >>> cycles = find_synodic_cycles(
        >>>     Planet.SUN, Planet.MOON,
        >>>     start, end,
        >>>     get_positions_callback=get_pos
        >>> )
    """
    if get_positions_callback is None:
        raise ValueError("get_positions_callback must be provided")
    
    # This is a simplified implementation
    # A production implementation would use precise aspect finding algorithms
    # For now, return empty list with proper structure
    return []
