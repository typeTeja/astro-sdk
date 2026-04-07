"""
Eclipse Search Example

This example demonstrates how to find solar and lunar eclipses
using the EventService and the deterministic Time class.
"""

from datetime import UTC, datetime

from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.services.event_service import EventService


def main():
    # 1. Initialize services
    eph = Ephemeris()
    event_service = EventService(eph)

    # 2. Define search starting point
    start_time = Time(datetime(2024, 1, 1, tzinfo=UTC))

    print("=" * 70)
    print("ECLIPSE SEARCH - 2024")
    print("=" * 70)
    print(f"Starting search from: {start_time.dt.date()}")
    print()

    # 3. Find Next Solar Eclipse
    print("SOLAR ECLIPSE")
    print("-" * 70)
    try:
        solar = event_service.find_next_solar_eclipse(start_time)
        peak_time = Time.from_julian_day(solar.peak_jd)

        print("Next Solar Eclipse found:")
        print(f"  Date (UTC):   {peak_time.dt}")
        print(f"  Julian Day:   {solar.peak_jd:.6f}")
        print(f"  Type:         {solar.type}")
        print(f"  Magnitude:    {solar.magnitude:.4f}")
        print(f"  Total/Annular: {'Yes' if solar.is_total else 'No'}")
    except Exception as e:
        print(f"Error finding solar eclipse: {e}")

    print()

    # 4. Find Next Lunar Eclipse
    print("LUNAR ECLIPSE")
    print("-" * 70)
    try:
        lunar = event_service.find_next_lunar_eclipse(start_time)
        peak_time = Time.from_julian_day(lunar.peak_jd)

        print("Next Lunar Eclipse found:")
        print(f"  Date (UTC):   {peak_time.dt}")
        print(f"  Julian Day:   {lunar.peak_jd:.6f}")
        print(f"  Type:         {lunar.type}")
        print(f"  Magnitude:    {lunar.magnitude:.4f}")
        print(f"  Total:         {'Yes' if lunar.is_total else 'No'}")
    except Exception as e:
        print(f"Error finding lunar eclipse: {e}")

    print()
    print("=" * 70)
    print("Note: AstroSDK uses Swiss Ephemeris high-precision global search.")

if __name__ == "__main__":
    main()
