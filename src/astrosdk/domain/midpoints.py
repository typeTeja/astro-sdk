"""
Midpoints Module

Calculate and analyze planetary midpoints - the halfway point between two planets.
Used extensively in Uranian astrology and for identifying sensitive degree areas.

Example:
    # Calculate midpoint between Sun and Moon
    midpoint = calculate_midpoint(sun_long=100.0, moon_long=200.0)
    # Result: 150.0° (halfway between)
    
    # Get all midpoints for a chart
    midpoints = calculate_all_midpoints(planet_positions)
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from ..core.constants import Planet, ZodiacSign


class Midpoint(BaseModel):
    """
    Planetary midpoint calculation.
    
    The midpoint is the halfway point between two planets on the zodiac circle.
    Can be calculated in two directions (near and far).
    """
    model_config = ConfigDict(frozen=True)
    
    planet1: Planet
    planet2: Planet
    planet1_longitude: float = Field(ge=0.0, lt=360.0)
    planet2_longitude: float = Field(ge=0.0, lt=360.0)
    midpoint_longitude: float = Field(ge=0.0, lt=360.0, description="Near midpoint (shorter arc)")
    far_midpoint_longitude: float = Field(ge=0.0, lt=360.0, description="Far midpoint (longer arc)")
    
    @property
    def sign(self) -> ZodiacSign:
        """Zodiac sign of the near midpoint."""
        return ZodiacSign(int(self.midpoint_longitude / 30))
    
    @property
    def sign_degree(self) -> float:
        """Degree within the zodiac sign (0-30)."""
        return self.midpoint_longitude % 30.0
    
    @property
    def far_sign(self) -> ZodiacSign:
        """Zodiac sign of the far midpoint."""
        return ZodiacSign(int(self.far_midpoint_longitude / 30))
    
    def __str__(self) -> str:
        """String representation: A/B = 15° Aries."""
        return f"{self.planet1.name}/{self.planet2.name} = {self.sign_degree:.2f}° {self.sign.name}"


class MidpointTree(BaseModel):
    """
    Sorted list of midpoints in zodiacal order.
    
    Used for identifying clusters of midpoints and sensitive degree areas.
    """
    model_config = ConfigDict(frozen=True)
    
    midpoints: List[Midpoint]
    
    def get_by_longitude_range(self, min_long: float, max_long: float) -> List[Midpoint]:
        """
        Get midpoints within a longitude range.
        
        Args:
            min_long: Minimum longitude (0-360)
            max_long: Maximum longitude (0-360)
        
        Returns:
            List of midpoints in range
        """
        result = []
        for mp in self.midpoints:
            if min_long <= max_long:
                if min_long <= mp.midpoint_longitude <= max_long:
                    result.append(mp)
            else:  # Wraparound
                if mp.midpoint_longitude >= min_long or mp.midpoint_longitude <= max_long:
                    result.append(mp)
        return result
    
    def get_clusters(self, orb: float = 2.0) -> List[List[Midpoint]]:
        """
        Identify clusters of midpoints within orb.
        
        Args:
            orb: Maximum separation for cluster (default 2°)
        
        Returns:
            List of midpoint clusters
        """
        if not self.midpoints:
            return []
        
        # Sort by longitude
        sorted_mp = sorted(self.midpoints, key=lambda m: m.midpoint_longitude)
        
        clusters = []
        current_cluster = [sorted_mp[0]]
        
        for mp in sorted_mp[1:]:
            if mp.midpoint_longitude - current_cluster[-1].midpoint_longitude <= orb:
                current_cluster.append(mp)
            else:
                if len(current_cluster) > 1:
                    clusters.append(current_cluster)
                current_cluster = [mp]
        
        if len(current_cluster) > 1:
            clusters.append(current_cluster)
        
        return clusters


def calculate_midpoint(long1: float, long2: float) -> tuple[float, float]:
    """
    Calculate near and far midpoints between two longitudes.
    
    Args:
        long1: First longitude (0-360)
        long2: Second longitude (0-360)
    
    Returns:
        Tuple of (near_midpoint, far_midpoint)
    
    Examples:
        >>> calculate_midpoint(0, 90)
        (45.0, 225.0)
        >>> calculate_midpoint(350, 10)
        (0.0, 180.0)
    """
    # Calculate angular separation
    diff = abs(long2 - long1)
    
    if diff <= 180:
        # Near midpoint is halfway through shorter arc
        near_mid = (long1 + long2) / 2.0
        far_mid = (near_mid + 180.0) % 360.0
    else:
        # Near midpoint is on opposite side
        near_mid = ((long1 + long2) / 2.0 + 180.0) % 360.0
        far_mid = (near_mid + 180.0) % 360.0
    
    return (near_mid, far_mid)


def calculate_all_midpoints(positions: List) -> MidpointTree:
    """
    Calculate all planetary midpoints for a chart.
    
    Args:
        positions: List of PlanetPosition objects
    
    Returns:
        MidpointTree with all midpoints sorted by longitude
    
    Example:
        >>> from astrosdk import calculate_natal_chart
        >>> chart = calculate_natal_chart(...)
        >>> midpoints = calculate_all_midpoints(chart.planets)
        >>> 
        >>> # Find Sun/Moon midpoint
        >>> sun_moon = [m for m in midpoints.midpoints 
        >>>             if {m.planet1, m.planet2} == {Planet.SUN, Planet.MOON}]
    """
    midpoints = []
    
    # Calculate all pairs
    for i, p1 in enumerate(positions):
        for p2 in positions[i+1:]:
            near, far = calculate_midpoint(p1.longitude, p2.longitude)
            
            midpoint = Midpoint(
                planet1=p1.planet,
                planet2=p2.planet,
                planet1_longitude=p1.longitude,
                planet2_longitude=p2.longitude,
                midpoint_longitude=near,
                far_midpoint_longitude=far
            )
            midpoints.append(midpoint)
    
    # Sort by near midpoint longitude
    midpoints_sorted = sorted(midpoints, key=lambda m: m.midpoint_longitude)
    
    return MidpointTree(midpoints=midpoints_sorted)


def find_midpoint_aspects(
    midpoints: List[Midpoint],
    target_longitude: float,
    orb: float = 1.0
) -> List[Midpoint]:
    """
    Find midpoints that aspect a target longitude.
    
    Useful for finding which midpoints are activated by a transiting planet
    or natal planet position.
    
    Args:
        midpoints: List of midpoints to search
        target_longitude: Target degree (0-360)
        orb: Maximum orb for conjunction (default 1.0°)
    
    Returns:
        List of midpoints within orb of target
    
    Example:
        >>> # Find midpoints at 15° Aries (15°)
        >>> activated = find_midpoint_aspects(all_midpoints, 15.0, orb=2.0)
        >>> for mp in activated:
        >>>     print(f"{mp.planet1}/{mp.planet2} at {mp.midpoint_longitude:.2f}°")
    """
    result = []
    
    for mp in midpoints:
        # Check near midpoint
        separation = abs(mp.midpoint_longitude - target_longitude)
        if separation > 180:
            separation = 360 - separation
        
        if separation <= orb:
            result.append(mp)
    
    return result
