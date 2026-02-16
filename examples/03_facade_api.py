"""
Example: Using the New Facade API (v1.3.0)

This demonstrates the clean, Pythonic API introduced in v1.3.0
"""

from astrosdk import (
    calculate_natal_chart,
    calculate_aspects,
    find_next_solar_eclipse,
    calculate_sunrise_sunset,
    AstroTime,
    Planet,
    HouseSystem,
    SiderealMode
)

# ============================================================================
# Example 1: Simple Natal Chart
# ============================================================================

print("=" * 60)
print("Example 1: Calculate a Natal Chart")
print("=" * 60)

# Create time (timezone-aware, enforced)
birth_time = AstroTime.from_components(
    year=1990,
    month=6,
    day=15,
    hour=14,
    minute=30,
    tz="America/New_York"
)

# Calculate chart (single function call)
chart = calculate_natal_chart(
    time=birth_time,
    latitude=40.7128,
    longitude=-74.0060,
    house_system=HouseSystem.PLACIDUS,
    sidereal_mode=SiderealMode.LAHIRI
)

# Access data (fully typed Pydantic models)
print(f"\nChart Time: {chart.time.dt}")
print(f"House System: {chart.houses.system.name}")
print(f"\nPlanetary Positions:")
for p in chart.planets[:5]:  # First 5 planets
    print(f"  {p.planet.name:12} {p.longitude:7.2f}° in {p.sign.name} "
          f"({'R' if p.is_retrograde else 'D'})")

print(f"\nAscendant: {chart.houses.axes.ascendant:.2f}°")
print(f"Midheaven: {chart.houses.axes.midheaven:.2f}°")


# ============================================================================
# Example 2: Aspect Calculation
# ============================================================================

print("\n" + "=" * 60)
print("Example 2: Calculate Aspects")
print("=" * 60)

aspects = calculate_aspects(chart.planets)

print(f"\nFound {len(aspects)} aspects:")
for asp in aspects[:5]:  # Show first 5
    print(f"  {asp.p1.name} {asp.type} {asp.p2.name} "
          f"(orb: {asp.orb:.2f}°, {'applying' if asp.applying else 'separating'})")


# ============================================================================
# Example 3: Find Next Eclipse
# ============================================================================

print("\n" + "=" * 60)
print("Example 3: Find Next Solar Eclipse")
print("=" * 60)

start = AstroTime.from_iso("2024-01-01T00:00:00Z")
next_eclipse = find_next_solar_eclipse(start)

if next_eclipse:
    print(f"\nNext solar eclipse: {next_eclipse.datetime}")


# ============================================================================
# Example 4: Sunrise/Sunset
# ============================================================================

print("\n" + "=" * 60)
print("Example 4: Sunrise and Sunset Times")
print("=" * 60)

today = AstroTime.from_components(2024, 6, 21, 0, 0, tz="UTC")
sun_times = calculate_sunrise_sunset(
    time=today,
    latitude=51.5074,  # London
    longitude=-0.1278
)

print(f"\nLondon, June 21, 2024:")
print(f"  Sunrise: {sun_times['sunrise'].datetime if sun_times['sunrise'] else 'N/A'}")
print(f"  Sunset:  {sun_times['sunset'].datetime if sun_times['sunset'] else 'N/A'}")


# ============================================================================
# Example 5: Tropical vs Sidereal
# ============================================================================

print("\n" + "=" * 60)
print("Example 5: Tropical vs Sidereal Comparison")
print("=" * 60)

time = AstroTime.from_components(2000, 1, 1, 12, 0, tz="UTC")

# Tropical (sidereal_mode=None)
tropical_chart = calculate_natal_chart(
    time, 40.7128, -74.0060,
    sidereal_mode=None  # Tropical
)

# Sidereal (Lahiri)
sidereal_chart = calculate_natal_chart(
    time, 40.7128, -74.0060,
    sidereal_mode=SiderealMode.LAHIRI
)

print("\nSun Position:")
print(f"  Tropical: {tropical_chart.planets[0].longitude:.2f}° "
      f"({tropical_chart.planets[0].sign.name})")
print(f"  Sidereal: {sidereal_chart.planets[0].longitude:.2f}° "
      f"({sidereal_chart.planets[0].sign.name})")
print(f"  Ayanamsa: {tropical_chart.planets[0].longitude - sidereal_chart.planets[0].longitude:.2f}°")


print("\n" + "=" * 60)
print("[SUCCESS] All examples completed successfully!")
print("=" * 60)
