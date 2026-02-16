"""
Primary Directions Module

Calculate primary directed positions using the "arc of direction" method.
Primary directions are a classical predictive technique based on the daily rotation of Earth.

1 degree of arc ≈ 1 year of life

Example:
    # Calculate Sun's directed position at age 30
    directed_sun = calculate_primary_direction(
        natal_longitude=100.0,
        age_years=30.0,
        method="direct"
    )
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, List
from datetime import datetime, timedelta
from ..core.constants import Planet


class DirectedPosition(BaseModel):
    """
    Planet position advanced by primary direction.
    
    Based on symbolic arc movement (1° ≈ 1 year).
    """
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    natal_longitude: float = Field(ge=0.0, lt=360.0)
    directed_longitude: float = Field(ge=0.0, lt=360.0)
    arc_degrees: float = Field(description="Arc of direction in degrees")
    age_years: float = Field(ge=0.0, description="Age in years")
    method: Literal["direct", "converse"] = "direct"
    
    @property
    def arc_years(self) -> float:
        """Convert arc to years (1° = 1 year)."""
        return self.arc_degrees


class TimeLordPeriod(BaseModel):
    """
    Time lord period for Firdaria or other systems.
    
    Time lord systems allocate planetary rulership to different life periods.
    """
    model_config = ConfigDict(frozen=True)
    
    planet: Planet
    start_age: float
    end_age: float
    start_date: datetime
    end_date: datetime
    level: int = Field(ge=1, le=2, description="1=major period, 2=sub-period")


def calculate_primary_direction(
    natal_longitude: float,
    age_years: float,
    method: Literal["direct", "converse"] = "direct"
) -> float:
    """
    Calculate directed longitude using primary directions.
    
    Args:
        natal_longitude: Natal position (0-360)
        age_years: Age in years to direct to
        method: "direct" (forward) or "converse" (backward)
    
    Returns:
        Directed longitude (0-360)
    
    Examples:
        >>> # Direct Sun at 100° to age 30
        >>> calculate_primary_direction(100.0, 30.0, "direct")
        130.0
        >>> 
        >>> # Converse Sun at 100° to age 30
        >>> calculate_primary_direction(100.0, 30.0, "converse")
        70.0
    """
    # Primary direction: 1 degree per year
    arc = age_years
    
    if method == "direct":
        directed = (natal_longitude + arc) % 360.0
    else:  # converse
        directed = (natal_longitude - arc) % 360.0
    
    return directed


def calculate_all_primary_directions(
    natal_positions: List,
    age_years: float,
    method: Literal["direct", "converse"] = "direct"
) -> List[DirectedPosition]:
    """
    Calculate primary directions for all planets.
    
    Args:
        natal_positions: List of natal PlanetPosition objects
        age_years: Age in years
        method: "direct" or "converse"
    
    Returns:
        List of DirectedPosition objects
    
    Example:
        >>> from astrosdk import calculate_natal_chart
        >>> natal = calculate_natal_chart(...)
        >>> 
        >>> # Get directed positions at age 45
        >>> directed = calculate_all_primary_directions(natal.planets, 45.0)
        >>> for d in directed:
        >>>     print(f"{d.planet.name}: {d.natal_longitude:.1f}° → {d.directed_longitude:.1f}°")
    """
    results = []
    
    for natal_pos in natal_positions:
        directed_long = calculate_primary_direction(
            natal_pos.longitude,
            age_years,
            method
        )
        
        arc = age_years if method == "direct" else -age_years
        
        result = DirectedPosition(
            planet=natal_pos.planet,
            natal_longitude=natal_pos.longitude,
            directed_longitude=directed_long,
            arc_degrees=arc,
            age_years=age_years,
            method=method
        )
        results.append(result)
    
    return results


def calculate_firdaria(
    birth_date: datetime,
    is_day_birth: bool = True
) -> List[TimeLordPeriod]:
    """
    Calculate Firdaria time lord periods.
    
    Firdaria is a Medieval timing technique that assigns planetary rulers
    to sequential life periods.
    
    Day birth order: Sun → Venus → Mercury → Moon → Saturn → Jupiter → Mars
    Night birth order: Moon → Saturn → Jupiter → Mars → Sun → Venus → Mercury
    
    Args:
        birth_date: Date and time of birth
        is_day_birth: True if born during day (Sun above horizon)
    
    Returns:
        List of TimeLordPeriod objects
    
    Note:
        This is a simplified implementation. Full Firdaria includes sub-periods.
    """
    # Simplified period lengths (years)
    day_sequence = [
        (Planet.SUN, 10),
        (Planet.VENUS, 8),
        (Planet.MERCURY, 13),
        (Planet.MOON, 9),
        (Planet.SATURN, 11),
        (Planet.JUPITER, 12),
        (Planet.MARS, 7)
    ]
    
    night_sequence = [
        (Planet.MOON, 9),
        (Planet.SATURN, 11),
        (Planet.JUPITER, 12),
        (Planet.MARS, 7),
        (Planet.SUN, 10),
        (Planet.VENUS, 8),
        (Planet.MERCURY, 13)
    ]
    
    sequence = day_sequence if is_day_birth else night_sequence
    
    periods = []
    current_age = 0.0
    current_date = birth_date
    
    for planet, duration in sequence:
        end_age = current_age + duration
        end_date = birth_date + timedelta(days=duration * 365.25)
        
        period = TimeLordPeriod(
            planet=planet,
            start_age=current_age,
            end_age=end_age,
            start_date=current_date,
            end_date=end_date,
            level=1
        )
        periods.append(period)
        
        current_age = end_age
        current_date = end_date
    
    return periods
