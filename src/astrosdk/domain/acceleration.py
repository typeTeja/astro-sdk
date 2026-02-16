"""
Planetary Acceleration - Second derivative of motion

Acceleration represents the rate of change of velocity (speed), indicating
whether a planet is speeding up or slowing down in its motion. This is
particularly important for:
- Detecting retrograde stations (when acceleration crosses zero)
- Analyzing planetary strength in traditional astrology
- Precise ephemeris calculations for research

This module calculates acceleration by sampling planetary positions at
small time intervals (default: 1 day before and after).
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from ..core.constants import Planet


class AccelerationData(BaseModel):
    """
    Acceleration state for a planetary body.
    
    Represents the second derivative of position with respect to time.
    """
    model_config = ConfigDict(frozen=True)
    
    longitude_accel: float = Field(description="Longitudinal acceleration (degrees/day²)")
    latitude_accel: float = Field(description="Latitudinal acceleration (degrees/day²)")
    distance_accel: float = Field(description="Radial acceleration (AU/day²)")
    
    @property
    def is_accelerating(self) -> bool:
        """True if planet is speeding up in longitude (acceleration > 0)."""
        return self.longitude_accel > 0
    
    @property
    def is_decelerating(self) -> bool:
        """True if planet is slowing down in longitude (acceleration < 0)."""
        return self.longitude_accel < 0
    
    @property
    def is_near_station(self) -> bool:
        """
        True if longitudinal acceleration is near zero (within 0.01 degrees/day²).
        
        This indicates the planet is near a retrograde station point
        (transition between direct and retrograde motion).
        """
        return abs(self.longitude_accel) < 0.01


def calculate_acceleration(
    position_before,
    position_current,
    position_after,
    time_delta: float = 1.0
) -> AccelerationData:
    """
    Calculate planetary acceleration from three position samples.
    
    Uses finite difference method to compute the second derivative:
    acceleration = (v_after - v_before) / (2 * time_delta)
    
    Where v = velocity (speed) at each time point.
    
    Args:
        position_before: PlanetPosition at (t - time_delta)
        position_current: PlanetPosition at (t) [for reference]
        position_after: PlanetPosition at (t + time_delta)
        time_delta: Time interval in days (default: 1.0)
    
    Returns:
        AccelerationData with longitude, latitude, and distance acceleration
    
    Notes:
        - Smaller time_delta gives more precise instantaneous acceleration
        - Larger time_delta smooths out short-term fluctuations
        - Default 1 day is suitable for most astrological purposes
    
    Examples:
        >>> # Planet slowing down before retrograde station
        >>> accel = calculate_acceleration(pos_yesterday, pos_today, pos_tomorrow)
        >>> accel.is_decelerating
        True
        >>> accel.is_near_station
        True  # If very close to station point
    """
    # Calculate acceleration for each coordinate
    # accel = (speed_after - speed_before) / (2 * dt)
    
    lon_accel = (position_after.speed_long - position_before.speed_long) / (2 * time_delta)
    lat_accel = (position_after.speed_lat - position_before.speed_lat) / (2 * time_delta)
    dist_accel = (position_after.speed_dist - position_before.speed_dist) / (2 * time_delta)
    
    return AccelerationData(
        longitude_accel=lon_accel,
        latitude_accel=lat_accel,
        distance_accel=dist_accel
    )


def calculate_acceleration_from_ephemeris(
    ephemeris,
    time,
    planet: Planet,
    time_delta_days: float = 1.0,
    sidereal_mode=None
) -> AccelerationData:
    """
    Calculate acceleration by querying ephemeris at three time points.
    
    This is a convenience function that handles the ephemeris queries
    automatically. It calculates positions at (t-delta, t, t+delta) and
    derives acceleration.
    
    Args:
        ephemeris: Ephemeris instance
        time: Time object for central calculation point
        planet: Planet to calculate acceleration for
        time_delta_days: Time interval in days (default: 1.0)
        sidereal_mode: Optional sidereal mode for calculations
    
    Returns:
        AccelerationData for the planet at the given time
    
    Examples:
        >>> from astrosdk.core.ephemeris import Ephemeris
        >>> from astrosdk.core.time import Time
        >>> from astrosdk.core.constants import Planet
        >>> 
        >>> eph = Ephemeris()
        >>> time = Time.from_components(2024, 1, 1, 12, 0, tz="UTC")
        >>> accel = calculate_acceleration_from_ephemeris(eph, time, Planet.MERCURY)
        >>> print(f"Mercury acceleration: {accel.longitude_accel:.4f} deg/day²")
    """
    from ..core.time import Time
    from datetime import timedelta
    
    # Calculate Julian Days for the three time points
    jd_before = time.julian_day - time_delta_days
    jd_current = time.julian_day
    jd_after = time.julian_day + time_delta_days
    
    # Query ephemeris for positions
    is_sidereal = sidereal_mode is not None
    
    pos_before_data = ephemeris.calculate_planet(
        jd_before, planet, sidereal=is_sidereal
    )
    pos_current_data = ephemeris.calculate_planet(
        jd_current, planet, sidereal=is_sidereal
    )
    pos_after_data = ephemeris.calculate_planet(
        jd_after, planet, sidereal=is_sidereal
    )
    
    # Create minimal position objects (we only need speeds)
    from ..domain.planet import PlanetPosition
    
    pos_before = PlanetPosition(
        planet=planet,
        longitude=pos_before_data["longitude"],
        latitude=pos_before_data["latitude"],
        distance=pos_before_data["distance"],
        speed_long=pos_before_data["speed_long"],
        speed_lat=pos_before_data["speed_lat"],
        speed_dist=pos_before_data["speed_dist"]
    )
    
    pos_current = PlanetPosition(
        planet=planet,
        longitude=pos_current_data["longitude"],
        latitude=pos_current_data["latitude"],
        distance=pos_current_data["distance"],
        speed_long=pos_current_data["speed_long"],
        speed_lat=pos_current_data["speed_lat"],
        speed_dist=pos_current_data["speed_dist"]
    )
    
    pos_after = PlanetPosition(
        planet=planet,
        longitude=pos_after_data["longitude"],
        latitude=pos_after_data["latitude"],
        distance=pos_after_data["distance"],
        speed_long=pos_after_data["speed_long"],
        speed_lat=pos_after_data["speed_lat"],
        speed_dist=pos_after_data["speed_dist"]
    )
    
    return calculate_acceleration(pos_before, pos_current, pos_after, time_delta_days)
