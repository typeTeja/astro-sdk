"""
AstroSDK 2.0 Example: Service Layer Direct Usage
Demonstrates how to use the underlying Python services without the API layer.
Ideal for library-based research and offline processing.
"""
from datetime import datetime, UTC
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.core.constants import Planet, SiderealMode
from app.contexts.factories import create_default_context
from app.services.astronomy.planetary_service import AstronomyPlanetaryService
from app.services.western import WesternChartService

def run_service_example():
    # 1. Initialize the singleton Ephemeris
    ephemeris = Ephemeris()
    
    # 2. Build a 2.0 CalculationContext
    context = create_default_context()
    context.zodiac.sidereal_mode = SiderealMode.LAHIRI
    
    print(f"Engine Context Initialized: {context.fingerprint}")
    
    # 3. Use the Planetary Service directly
    time = Time(datetime(2024, 4, 8, 18, 20, 48, tzinfo=UTC))
    planetary_service = AstronomyPlanetaryService(context, ephemeris)
    
    # Batch calculate specific planets
    targets = [Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS, Planet.MARS]
    snapshots = planetary_service.calculate_positions(time, targets)
    
    print("\n--- Planetary Positions (Service Layer) ---")
    for s in snapshots:
        status = "RETROGRADE" if s.is_retrograde else "DIRECT"
        print(f"{s.planet.name:<10}: {s.longitude:>10.4f}° | {status}")

    # 4. Use the Western Chart Service
    chart_service = WesternChartService(context, ephemeris)
    # New York City Coordinates
    chart = chart_service.create_chart(time, lat=40.7128, lon=-74.0060)
    
    print("\n--- Western Chart Houses ---")
    if chart.houses:
        print(f"House System: {chart.houses.system.name}")
        for cusp in chart.houses.cusps:
            print(f"House {cusp.number:<2}: {cusp.longitude:>10.4f}° ({cusp.sign.name})")

if __name__ == "__main__":
    run_service_example()
