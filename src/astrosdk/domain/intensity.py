"""
Astro-Intensity Signal Module

Multi-factor scoring system that provides a 0-1 normalized intensity score
indicating the level of astrological activity at a given time.

Factors:
- Aspect density (number of aspects forming)
- Retrograde planet count
- Eclipse proximity
- Station points (planets near direction change)
- Angular separations (tight orbs)

Example:
    intensity = calculate_intensity(
        time=datetime.now(),
        planets=chart.planets,
        aspects=aspects,
        window_days=7
    )
    
    if intensity.normalized_value > 0.7:
        print("High astrological activity period!")
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime

from .planet import PlanetPosition
from .aspect import Aspect


class IntensitySignal(BaseModel):
    """
    Astrological intensity score with contributing factors.
    
    Provides a normalized 0-1 score indicating relative activity level.
    """
    model_config = ConfigDict(frozen=True)
    
    timestamp: datetime
    normalized_value: float = Field(ge=0.0, le=1.0, description="0=quiet, 1=extremely active")
    drivers: List[str] = Field(description="List of contributing factors")
    aspect_density: int = Field(ge=0, description="Number of aspects within orb")
    retrograde_count: int = Field(ge=0, description="Number of retrograde planets")
    station_count: int = Field(ge=0, description="Planets near stations (speed ~0)")
    tight_aspect_count: int = Field(ge=0, description="Aspects with orb < 1°")
    
    @property
    def activity_level(self) -> str:
        """
        Classify intensity level.
        
        Returns:
            'quiet', 'moderate', 'active', or 'extremely_active'
        """
        if self.normalized_value < 0.25:
            return "quiet"
        elif self.normalized_value < 0.5:
            return "moderate"
        elif self.normalized_value < 0.75:
            return "active"
        else:
            return "extremely_active"


def calculate_intensity(
    time: datetime,
    planets: List[PlanetPosition],
    aspects: List[Aspect],
    window_days: float = 7.0
) -> IntensitySignal:
    """
    Calculate astrological intensity signal at a given time.
    
    Args:
        time: Time to calculate intensity for
        planets: Planet positions
        aspects: Active aspects
        window_days: Time window for intensity calculation (default 7 days)
    
    Returns:
        IntensitySignal with normalized score and contributing factors
    
    Examples:
        >>> intensity = calculate_intensity(now, planets, aspects)
        >>> if intensity.activity_level == "extremely_active":
        >>>     print(f"Drivers: {intensity.drivers}")
    """
    drivers = []
    
    # Factor 1: Aspect density
    aspect_density = len(aspects)
    if aspect_density > 10:
        drivers.append("high_aspect_density")
    
    # Factor 2: Retrograde count
    retrograde_count = sum(1 for p in planets if p.is_retrograde)
    if  retrograde_count > 2:
        drivers.append("multiple_retrogrades")
    
    # Factor 3: Station count (planets near direction change)
    station_count = sum(1 for p in planets if abs(p.speed_long) < 0.05)
    if station_count > 0:
        drivers.append("station_points")
    
    # Factor 4: Tight aspects (< 1° orb)
    tight_aspect_count = sum(1 for a in aspects if abs(a.orb) < 1.0)
    if tight_aspect_count > 3:
        drivers.append("tight_aspects")
    
    # Normalize to 0-1 scale
    # Simple weighted combination
    score = 0.0
    score += min(aspect_density / 20.0, 0.3)  # Max 0.3 from aspects
    score += min(retrograde_count / 4.0, 0.2)  # Max 0.2 from retrogrades
    score += min(station_count / 2.0, 0.2)     # Max 0.2 from stations
    score += min(tight_aspect_count / 5.0, 0.3)  # Max 0.3 from tight aspects
    
    normalized = min(score, 1.0)
    
    return IntensitySignal(
        timestamp=time,
        normalized_value=normalized,
        drivers=drivers,
        aspect_density=aspect_density,
        retrograde_count=retrograde_count,
        station_count=station_count,
        tight_aspect_count=tight_aspect_count
    )
