"""
AstroSDK 2.0 Example: Advanced Chart Configurations
Demonstrates Heliocentric, Topocentric, and Sidereal overrides.
"""
from datetime import datetime, UTC
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.core.constants import Planet, SiderealMode, HouseSystem
from app.contexts.factories import create_default_context
from app.services.western import WesternChartService

def run_advanced_example():
    ephemeris = Ephemeris()
    time = Time(datetime(2024, 4, 8, 18, 0, 0, tzinfo=UTC))
    
    # --- Case 1: Heliocentric (Sun-Centered) Model ---
    helio_ctx = create_default_context()
    helio_ctx.coordinate.system = "heliocentric"
    helio_ctx.zodiac.zodiac = "tropical" # Usually used for helio
    
    helio_service = WesternChartService(helio_ctx, ephemeris)
    helio_chart = helio_service.create_chart(time, lat=0, lon=0)
    
    print("\n--- 1. Heliocentric Solar System Positions ---")
    for s in helio_chart.planets:
        print(f"{s.planet.name:<10}: {s.longitude:>10.4f}°")

    # --- Case 2: High-Precision Topocentric Calculations ---
    # Observer in Torreón, Mexico (Total Eclipse Center)
    topo_ctx = create_default_context()
    topo_ctx.coordinate.system = "topocentric"
    topo_ctx.observer.latitude = 25.5439
    topo_ctx.observer.longitude = -103.4190
    topo_ctx.observer.altitude = 1120
    topo_ctx.house.system = HouseSystem.PLACIDUS
    
    topo_service = WesternChartService(topo_ctx, ephemeris)
    topo_chart = topo_service.create_chart(time, lat=25.5439, lon=-103.4190)
    
    print("\n--- 2. Topocentric Chart (Total Eclipse Observer) ---")
    print(f"Calculation Fingerprint: {topo_ctx.fingerprint}")
    if topo_chart.houses:
        print(f"Topocentric Ascendant: {topo_chart.houses.axes.ascendant:.4f}°")
    
    # Find Moon's topocentric longitude
    moon = next(p for p in topo_chart.planets if p.planet == Planet.MOON)
    print(f"Topocentric Moon:      {moon.longitude:.4f}°")

if __name__ == "__main__":
    run_advanced_example()
