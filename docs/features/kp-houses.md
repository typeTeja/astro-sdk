# KP House System

The Krishnamurti Paddhati (KP) system is an advanced house division method that provides three levels of planetary rulership for each house cusp.

## Overview

KP system adds precision to house analysis through:

- **Sign Lord**: Traditional sign ruler
- **Star Lord (Nakshatra)**: Lunar mansion ruler (27 divisions)
- **Sub-Lord**: Vimshottari dasha sub-period ruler

This 3-tier system allows for more precise timing and interpretation.

## Basic Usage

```python
from astrosdk import calculate_natal_chart
from astrosdk.domain.kp_houses import calculate_kp_houses

# Calculate natal chart (Placidus)
chart = calculate_natal_chart(time, latitude, longitude)

# Extract Placidus cusps
placidus_cusps = [cusp.longitude for cusp in chart.houses.cusps]

# Convert to KP system
kp_system = calculate_kp_houses(
    house_cusps=placidus_cusps,
    ascendant=chart.houses.axes.ascendant,
    midheaven=chart.houses.axes.midheaven
)
```

## Accessing KP Data

```python
# Iterate through houses
for cusp in kp_system.cusps:
    print(f"House {cusp.house_number}:")
    print(f"  Longitude: {cusp.longitude:.2f}°")
    print(f"  Sign Lord: {cusp.sign_lord.name}")
    print(f"  Star Lord: {cusp.star_lord.name}")
    print(f"  Sub-Lord: {cusp.sub_lord.name}")
```

## Nakshatra System

The 27 Nakshatras divide the zodiac into 13°20' segments:

```python
from astrosdk.domain.kp_houses import get_nakshatra_lord

# Get nakshatra lord for any longitude
longitude = 125.5  # 5°30' Leo
nakshatra_lord = get_nakshatra_lord(longitude)
print(f"Nakshatra Lord: {nakshatra_lord.name}")
```

## Sub-Lord Calculation

Sub-lords use Vimshottari dasha proportions:

```python
from astrosdk.domain.kp_houses import get_sub_lord

# Get sub-lord for any longitude
sub_lord = get_sub_lord(longitude)
print(f"Sub-Lord: {sub_lord.name}")
```

## Practical Example

```python
from astrosdk import calculate_natal_chart, AstroTime
from astrosdk.domain.kp_houses import calculate_kp_houses

# Birth data
time = AstroTime.from_components(1990, 1, 1, 12, 0, tz="UTC")
lat, lon = 28.6139, 77.2090  # New Delhi

# Calculate chart
chart = calculate_natal_chart(time, lat, lon)

# Get KP houses
cusps = [c.longitude for c in chart.houses.cusps]
kp = calculate_kp_houses(cusps, chart.houses.axes.ascendant, chart.houses.axes.midheaven)

# Analyze 7th house (partnerships)
house_7 = kp.cusps[6]  # 0-indexed
print(f"7th House Analysis:")
print(f"  Sign Lord: {house_7.sign_lord.name}")
print(f"  Star Lord: {house_7.star_lord.name}")
print(f"  Sub-Lord: {house_7.sub_lord.name}")
```

## Interpretation Guidelines

### Sign Lord
- Indicates general nature of house matters
- Traditional planetary rulership

### Star Lord (Nakshatra)
- Adds lunar mansion influence
- 27-fold division for precision
- Connects to Vimshottari dasha system

### Sub-Lord
- Most precise level of analysis
- Based on proportional dasha periods
- Critical for timing predictions

## Technical Details

### Nakshatra Sequence
1. Ashwini (Ketu)
2. Bharani (Venus)
3. Krittika (Sun)
... (27 total)

### Dasha Periods (years)
- Ketu: 7
- Venus: 20
- Sun: 6
- Moon: 10
- Mars: 7
- Rahu: 18
- Jupiter: 16
- Saturn: 19
- Mercury: 17

**Total**: 120 years

## See Also

- [Houses Guide](../guide/houses.md) - General house systems
- [API Reference](../api/models.md) - KP model documentation
