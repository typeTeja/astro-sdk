"""
AstroSDK 2.0 Example: Batch Research Processing
Demonstrates how to use the 2.0 CalculationContext for high-throughput batch research.
This example scans a range of dates to find Mercury Retrograde entry/exit points.
"""
from datetime import datetime, timedelta, UTC
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.core.constants import Planet, SiderealMode
from app.contexts.factories import create_default_context
from app.services.astronomy.planetary_service import AstronomyPlanetaryService

def find_mercury_retrograde_events():
    ephemeris = Ephemeris()
    context = create_default_context()
    context.zodiac.sidereal_mode = SiderealMode.LAHIRI
    
    service = AstronomyPlanetaryService(context, ephemeris)
    
    start_date = datetime(2024, 7, 1, tzinfo=UTC)
    days_to_scan = 90
    
    print(f"Scanning Mercury Motion for {days_to_scan} days starting from {start_date.date()}...")
    print("-" * 60)
    print(f"{'Date':<20} | {'Longitude':<12} | {'Motion'}")
    print("-" * 60)
    
    last_retro = None
    
    for i in range(days_to_scan):
        current_date = start_date + timedelta(days=i)
        t = Time(current_date)
        
        # Calculate Mercury position
        pos = service.calculate_positions(t, [Planet.MERCURY])[0]
        
        # Detect state change
        is_retro = pos.is_retrograde
        if last_retro is not None and is_retro != last_retro:
            event_type = "ENTER RETROGRADE" if is_retro else "EXIT RETROGRADE"
            print(f"{current_date.strftime('%Y-%m-%d %H:%M'):<20} | {pos.longitude:>10.2f}° | *** {event_type} ***")
        
        last_retro = is_retro

if __name__ == "__main__":
    find_mercury_retrograde_events()
