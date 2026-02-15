"""
Basic Natal Chart Calculation Example

This example demonstrates how to calculate a natal chart
with planetary positions and house cusps.
"""

from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet, HouseSystem
from astrosdk.services.natal_service import NatalService

def main():
    # Initialize ephemeris
    eph = Ephemeris()
    natal_service = NatalService(eph)
    
    # Create birth time (must be timezone-aware)
    birth_time = Time(datetime(1990, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
    
    # Birth location (New York City)
    latitude = 40.7128
    longitude = -74.0060
    
    # Calculate natal chart
    chart = natal_service.calculate_natal_chart(
        time=birth_time,
        latitude=latitude,
        longitude=longitude,
        house_system=HouseSystem.PLACIDUS
    )
    
    # Display planetary positions
    print("=" * 60)
    print("NATAL CHART")
    print("=" * 60)
    print(f"Date: {birth_time.dt}")
    print(f"Location: {latitude}°N, {abs(longitude)}°W")
    print(f"Julian Day: {birth_time.julian_day:.6f}")
    print()
    
    print("PLANETARY POSITIONS")
    print("-" * 60)
    for planet_pos in chart.planets:
        retro = "⟲" if planet_pos.is_retrograde else " "
        print(f"{planet_pos.planet.name:12} {planet_pos.longitude:7.2f}° "
              f"{planet_pos.sign.name:12} {planet_pos.sign_degree:5.2f}° {retro}")
    
    # Display house cusps
    if chart.houses:
        print()
        print("HOUSE CUSPS")
        print("-" * 60)
        for cusp in chart.houses.cusps:
            print(f"House {cusp.number:2d}: {cusp.longitude:7.2f}° ({cusp.sign.name})")
        
        print()
        print("ANGLES")
        print("-" * 60)
        print(f"Ascendant:  {chart.houses.axes.ascendant:.2f}°")
        print(f"Midheaven:  {chart.houses.axes.midheaven:.2f}°")
        print(f"Descendant: {chart.houses.axes.descendant:.2f}°")
        print(f"IC:         {chart.houses.axes.imum_coeli:.2f}°")

if __name__ == "__main__":
    main()
