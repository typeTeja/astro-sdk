# Quick Start

Get up and running with AstroSDK in minutes.

## Installation

```bash
pip install astrosdk
```

## Your First Chart

```python
from astrosdk import calculate_natal_chart, AstroTime

# Create a timezone-aware time
time = AstroTime.from_components(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    tz="UTC"
)

# Calculate natal chart
chart = calculate_natal_chart(
    time=time,
    latitude=40.7128,   # New York City
    longitude=-74.0060,
    sidereal_mode=None  # None = Tropical
)

# Print planet positions
for planet in chart.planets:
    print(f"{planet.planet.name}:")
    print(f"  Longitude: {planet.longitude:.2f}°")
    print(f"  Sign: {planet.sign.name} {planet.sign_degree:.2f}°")
    if planet.is_retrograde:
        print(f"  ⟲ Retrograde")
```

## Calculate Aspects

```python
from astrosdk import calculate_aspects

# Calculate major aspects
aspects = calculate_aspects(chart.planets)

for aspect in aspects:
    print(f"{aspect.p1.name} {aspect.type} {aspect.p2.name}")
    print(f"  Orb: {aspect.orb:.2f}°")
    print(f"  {'Applying' if aspect.applying else 'Separating'}")
```

## Time Handling

AstroSDK enforces timezone-aware datetimes for determinism:

```python
# From components (recommended)
time = AstroTime.from_components(2024, 1, 15, 12, 0, tz="America/New_York")

# From ISO string
time = AstroTime.from_iso("2024-01-15T12:00:00-05:00")

# From datetime (must be timezone-aware)
from datetime import datetime
from zoneinfo import ZoneInfo

dt = datetime(2024, 1, 15, 12, 0, tzinfo=ZoneInfo("UTC"))
time = AstroTime(dt)
```

## Sidereal vs Tropical

```python
from astrosdk import SiderealMode

# Tropical (default)
chart_tropical = calculate_natal_chart(
    time=time,
    latitude=40.7,
    longitude=-74.0,
    sidereal_mode=None
)

# Sidereal (Lahiri)
chart_sidereal = calculate_natal_chart(
    time=time,
    latitude=40.7,
    longitude=-74.0,
    sidereal_mode=SiderealMode.LAHIRI
)

# Other ayanamsas
chart_kp = calculate_natal_chart(
    time=time,
    latitude=40.7,
    longitude=-74.0,
    sidereal_mode=SiderealMode.KRISHNAMURTI
)
```

## House Systems

```python
from astrosdk import HouseSystem

# Placidus (default)
chart = calculate_natal_chart(
    time=time,
    latitude=40.7,
    longitude=-74.0,
    house_system=HouseSystem.PLACIDUS
)

# Whole Sign
chart_whole = calculate_natal_chart(
    time=time,
    latitude=40.7,
    longitude=-74.0,
    house_system=HouseSystem.WHOLE_SIGN
)

# Access houses
for cusp in chart.houses.cusps:
    print(f"House {cusp.house_number}: {cusp.longitude:.2f}°")
```

## Next Steps

- [Core Concepts](concepts.md) - Understand key principles
- [Natal Charts Guide](../guide/natal-charts.md) - Deep dive into charts
- [Advanced Features](../features/kp-houses.md) - Explore KP Houses, Event Rules, etc.
- [API Reference](../api/public.md) - Complete API documentation
