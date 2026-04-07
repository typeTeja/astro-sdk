"""
Basic Natal Chart Calculation Example

This example demonstrates how to calculate a natal chart
with planetary positions and house cusps using the high-level ChartEngine.
"""

from datetime import UTC, datetime

from app.core.constants import HouseSystem, SiderealMode
from app.core.time import Time
from app.engine.chart_engine import ChartEngine


def main():
    # 1. Initialize the High-Level Engine
    # ChartEngine handles Ephemeris initialization and orchestration
    engine = ChartEngine()

    # 2. Create birth time (must be timezone-aware)
    birth_time = Time(datetime(1990, 1, 1, 12, 0, 0, tzinfo=UTC))

    # 3. Birth location (New York City)
    latitude = 40.7128
    longitude = -74.0060

    # 4. Generate the complete Chart object
    chart = engine.create_chart(
        time=birth_time,
        lat=latitude,
        lon=longitude,
        system=HouseSystem.PLACIDUS,
        sidereal_mode=SiderealMode.LAHIRI
    )

    # 5. Display basic metadata
    print("=" * 60)
    print("NATAL CHART")
    print("=" * 60)
    print(f"Date:       {chart.time.dt}")
    print(f"Location:   {latitude}°N, {abs(longitude)}°W")
    print(f"Ayanamsa:   {chart.metadata['sidereal_mode']}")
    print(f"Houses:     {chart.metadata['house_system']}")
    print()

    # 6. Display planetary positions including horizontal data
    print(f"{'PLANET':12} {'LONG':7} {'SIGN':12} {'DEG':5} {'AZ':7} {'ALT':7}")
    print("-" * 60)
    for p in chart.planets:
        retro = "⟲" if p.is_retrograde else " "
        az_str = f"{p.azimuth:7.2f}°" if p.azimuth is not None else "   N/A  "
        alt_str = f"{p.altitude:7.2f}°" if p.altitude is not None else "   N/A  "
        print(f"{p.planet.name:12} {p.longitude:7.2f}  {p.sign.name:12} {p.sign_degree:5.2f}° {az_str} {alt_str} {retro}")

    # 7. Display house cusps
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
