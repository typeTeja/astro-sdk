# Midpoints

Midpoints are the halfway points between two planets on the zodiac circle. They represent sensitive degrees that blend the energies of both planets.

## Overview

Midpoints are used extensively in:
- **Uranian Astrology** - Primary technique
- **Cosmobiology** - Ebertin's system
- **Sensitive Point Analysis** - Activation by transits

## Basic Usage

```python
from astrosdk import calculate_natal_chart
from astrosdk.domain.midpoints import calculate_all_midpoints

# Calculate chart
chart = calculate_natal_chart(time, latitude, longitude)

# Calculate all midpoints
midpoints = calculate_all_midpoints(chart.planets)

# Access midpoints (sorted by longitude)
for mp in midpoints.midpoints:
    print(f"{mp.planet1.name}/{mp.planet2.name}:")
    print(f"  Near: {mp.midpoint_longitude:.2f}°")
    print(f"  Far: {mp.far_midpoint_longitude:.2f}°")
    print(f"  Sign: {mp.sign.name} {mp.sign_degree:.2f}°")
```

## Finding Specific Midpoints

```python
from astrosdk.core.constants import Planet

# Find Sun/Moon midpoint
sun_moon = [m for m in midpoints.midpoints 
            if {m.planet1, m.planet2} == {Planet.SUN, Planet.MOON}][0]

print(f"Sun/Moon midpoint: {sun_moon.midpoint_longitude:.2f}°")
print(f"Sign: {sun_moon.sign.name}")
```

## Midpoint Activation

Find which midpoints are activated by a transit or natal planet:

```python
from astrosdk.domain.midpoints import find_midpoint_aspects

# Transit Mars at 150.0°
transit_longitude = 150.0

# Find activated midpoints (1° orb)
activated = find_midpoint_aspects(
    midpoints.midpoints,
    transit_longitude,
    orb=1.0
)

for mp in activated:
    print(f"{mp.planet1.name}/{mp.planet2.name} activated")
    print(f"  Midpoint: {mp.midpoint_longitude:.2f}°")
    print(f"  Transit: {transit_longitude:.2f}°")
```

## Midpoint Trees

Midpoints sorted by zodiacal order for pattern analysis:

```python
# Get midpoints in a longitude range
in_range = midpoints.get_by_longitude_range(140.0, 160.0)

print(f"Found {len(in_range)} midpoints between 140-160°")
for mp in in_range:
    print(f"  {mp.planet1.name}/{mp.planet2.name} at {mp.midpoint_longitude:.2f}°")
```

## Cluster Detection

Find clusters of midpoints (sensitive degree areas):

```python
# Find clusters within 2° orb
clusters = midpoints.get_clusters(orb=2.0)

for i, cluster in enumerate(clusters, 1):
    print(f"Cluster {i}:")
    for mp in cluster:
        print(f"  {mp.planet1.name}/{mp.planet2.name}: {mp.midpoint_longitude:.2f}°")
```

## Direct Midpoint Calculation

Calculate midpoint between any two longitudes:

```python
from astrosdk.domain.midpoints import calculate_midpoint

# Calculate midpoint between 100° and 200°
near, far = calculate_midpoint(100.0, 200.0)

print(f"Near midpoint: {near}°")  # 150.0°
print(f"Far midpoint: {far}°")    # 330.0°
```

## Practical Example: Transit Analysis

```python
from astrosdk import calculate_natal_chart, AstroTime
from astrosdk.domain.midpoints import calculate_all_midpoints, find_midpoint_aspects

# Natal chart
natal_time = AstroTime.from_components(1990, 1, 1, 12, 0, tz="UTC")
natal = calculate_natal_chart(natal_time, 40.7, -74.0)

# Calculate natal midpoints
natal_midpoints = calculate_all_midpoints(natal.planets)

# Transit chart
transit_time = AstroTime.from_components(2024, 6, 15, 12, 0, tz="UTC")
transit = calculate_natal_chart(transit_time, 40.7, -74.0)

# Check which natal midpoints are activated by transiting planets
for planet in transit.planets:
    activated = find_midpoint_aspects(
        natal_midpoints.midpoints,
        planet.longitude,
        orb=1.0
    )
    
    if activated:
        print(f"\nTransiting {planet.planet.name} at {planet.longitude:.2f}° activates:")
        for mp in activated:
            print(f"  {mp.planet1.name}/{mp.planet2.name}")
```

## Interpretation Guidelines

### Near vs Far Midpoints
- **Near Midpoint**: Shorter arc, primary interpretation
- **Far Midpoint**: Longer arc, secondary interpretation

### Orbs
- **Tight orb (0-1°)**: Strong activation
- **Medium orb (1-2°)**: Moderate activation
- **Wide orb (2-3°)**: Weak activation

### Midpoint Notation
- **A/B = C**: Planet C at midpoint of A and B
- Example: "Sun/Moon = Venus" means Venus conjuncts Sun/Moon midpoint

## See Also

- [Harmonic Charts](harmonics.md) - Related technique
- [Aspects Guide](../guide/aspects.md) - Understanding aspects
