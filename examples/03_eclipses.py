"""
Eclipse Search Example

This example demonstrates how to find solar and lunar eclipses
within a specific time range.
"""

from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.services.event_service import EventService

def main():
    # Initialize services
    eph = Ephemeris()
    event_service = EventService(eph)
    
    # Define search range (2024)
    start_time = Time(datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
    end_time = Time(datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
    
    print("=" * 70)
    print("ECLIPSE SEARCH - 2024")
    print("=" * 70)
    print(f"Search range: {start_time.dt.date()} to {end_time.dt.date()}")
    print()
    
    # Find next solar eclipse
    print("SOLAR ECLIPSES")
    print("-" * 70)
    try:
        solar_eclipse = event_service.find_next_solar_eclipse(start_time)
        eclipse_time = Time.from_string(
            f"{int(solar_eclipse.peak_jd)} 00:00:00",
            "%Y%j %H:%M:%S"
        )
        print(f"Next solar eclipse:")
        print(f"  Julian Day: {solar_eclipse.peak_jd:.6f}")
        print(f"  Type: {solar_eclipse.type}")
        print(f"  Total: {'Yes' if solar_eclipse.is_total else 'No'}")
    except Exception as e:
        print(f"Error finding solar eclipse: {e}")
    
    print()
    
    # Find next lunar eclipse
    print("LUNAR ECLIPSES")
    print("-" * 70)
    try:
        lunar_eclipse = event_service.find_next_lunar_eclipse(start_time)
        print(f"Next lunar eclipse:")
        print(f"  Julian Day: {lunar_eclipse.peak_jd:.6f}")
        print(f"  Type: {lunar_eclipse.type}")
        print(f"  Total: {'Yes' if lunar_eclipse.is_total else 'No'}")
    except Exception as e:
        print(f"Error finding lunar eclipse: {e}")
    
    print()
    print("=" * 70)
    print("Note: Use search range validation to prevent excessive searches")
    print("Maximum search range: 100 years (~36,525 days)")

if __name__ == "__main__":
    main()
