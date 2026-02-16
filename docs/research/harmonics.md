# Harmonic Charts

Harmonic charts multiply planetary positions to reveal hidden patterns and relationships. They're used to uncover talents, challenges, and life themes.

## Overview

Common harmonics:
- **H2**: Partnerships, polarities
- **H3**: Creativity, expression
- **H4**: Structure, foundation
- **H5**: Creativity, manifestation
- **H7**: Spiritual, inspirational
- **H9**: Completion, fulfillment

## Basic Usage

```python
from astrosdk import calculate_natal_chart
from astrosdk.domain.harmonics import calculate_harmonic_positions

# Calculate natal chart
chart = calculate_natal_chart(time, latitude, longitude)

# Generate 5th harmonic
h5 = calculate_harmonic_positions(chart.planets, harmonic=5)

# Access harmonic positions
for pos in h5.positions:
    print(f"{pos.planet.name}:")
    print(f"  Natal: {pos.natal_longitude:.2f}°")
    print(f"  H5: {pos.harmonic_longitude:.2f}°")
    print(f"  H5 Sign: {pos.sign.name}")
```

## Finding Harmonic Aspects

In harmonic charts, **conjunctions** are the primary aspect to examine:

```python
from astrosdk.domain.harmonics import find_harmonic_aspects

# Find conjunctions in H5 (2° orb)
aspects = find_harmonic_aspects(h5, orb=2.0)

for p1, p2, orb in aspects:
    print(f"{p1.name}-{p2.name} conjunction in H5")
    print(f"  Orb: {orb:.2f}°")
```

## Multiple Harmonics

Compare patterns across different harmonics:

```python
# Generate multiple harmonics
harmonics = {}
for h_num in [2, 3, 4, 5, 7, 9]:
    harmonics[h_num] = calculate_harmonic_positions(chart.planets, h_num)

# Check Sun-Moon relationship in each
from astrosdk.core.constants import Planet

for h_num, h_chart in harmonics.items():
    sun = h_chart.get_planet(Planet.SUN)
    moon = h_chart.get_planet(Planet.MOON)
    
    # Calculate separation
    sep = abs(sun.harmonic_longitude - moon.harmonic_longitude)
    if sep > 180:
        sep = 360 - sep
    
    print(f"H{h_num}: Sun-Moon separation = {sep:.2f}°")
```

## Direct Harmonic Calculation

Calculate harmonic longitude for any position:

```python
from astrosdk.domain.harmonics import calculate_harmonic_longitude

natal_long = 100.0  # 10° Cancer

# Calculate harmonics
h2 = calculate_harmonic_longitude(natal_long, 2)  # 200.0°
h5 = calculate_harmonic_longitude(natal_long, 5)  # 140.0°
h7 = calculate_harmonic_longitude(natal_long, 7)  # 340.0°

print(f"Natal: {natal_long}°")
print(f"H2: {h2}°")
print(f"H5: {h5}°")
print(f"H7: {h7}°")
```

## Practical Example

```python
from astrosdk import calculate_natal_chart, AstroTime
from astrosdk.domain.harmonics import calculate_harmonic_positions, find_harmonic_aspects

# Birth data
time = AstroTime.from_components(1990, 1, 1, 12, 0, tz="UTC")
chart = calculate_natal_chart(time, 40.7, -74.0)

# Generate H5 (creativity/manifestation)
h5 = calculate_harmonic_positions(chart.planets, 5)

# Find tight conjunctions (creative talents)
conjunctions = find_harmonic_aspects(h5, orb=1.0)

print("Creative Patterns (H5 conjunctions):")
for p1, p2, orb in conjunctions:
    print(f"  {p1.name}-{p2.name}: {orb:.2f}° orb")
```

## Interpretation Guidelines

### H2 (Duality)
- Partnerships
- Balance/imbalance
- Opposites attract

### H3 (Trinity)
- Creative expression
- Communication
- Mental activity

### H4 (Quaternary)
- Structure
- Foundation
- Material world

### H5 (Quintile)
- Talents
- Creativity
- Manifestation

### H7 (Septile)
- Spiritual insight
- Inspiration
- Fate/destiny

### H9 (Novile)
- Completion
- Fulfillment
- Spiritual attainment

## Advanced: Custom Harmonics

Any harmonic number is supported:

```python
# H12 (dodecile - 30° divisions)
h12 = calculate_harmonic_positions(chart.planets, 12)

# H16 (semi-semi-square emphasis)
h16 = calculate_harmonic_positions(chart.planets, 16)

# H360 (degree-by-degree)
h360 = calculate_harmonic_positions(chart.planets, 360)
```

## See Also

- [Midpoints](midpoints.md) - Related technique
- [Aspects Guide](../guide/aspects.md) - Understanding aspects
