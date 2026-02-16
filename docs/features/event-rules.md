# Event Rule Engine

The Event Rule Engine allows you to define custom astrological patterns using JSON-like rules and scan time ranges for matches.

## Overview

The engine supports 6 condition types that can be combined with AND/OR logic:

- **AspectCondition**: Planetary aspects
- **DignityCondition**: Essential dignities
- **CombustionCondition**: Combustion states
- **SpeedCondition**: Speed comparisons
- **RetrogradeCondition**: Retrograde motion
- **LongitudeCondition**: Longitude ranges

## Basic Example

```python
from astrosdk.domain.event_rules import (
    EventRule, RetrogradeCondition, LogicOperator
)
from astrosdk.core.constants import Planet

# Define rule: "Mercury is retrograde"
rule = EventRule(
    name="Mercury Retrograde",
    conditions=[
        RetrogradeCondition(
            planet=Planet.MERCURY,
            is_retrograde=True
        )
    ],
    logic=LogicOperator.AND
)
```

## Condition Types

### AspectCondition

```python
from astrosdk.domain.event_rules import AspectCondition

condition = AspectCondition(
    planet1=Planet.SUN,
    planet2=Planet.MARS,
    aspect_types=["CONJUNCTION", "OPPOSITION"],
    max_orb=5.0
)
```

### DignityCondition

```python
from astrosdk.domain.event_rules import DignityCondition
from astrosdk.domain.dignity import DignityType

condition = DignityCondition(
    planet=Planet.VENUS,
    dignity_types=[DignityType.RULER, DignityType.EXALTATION]
)
```

### CombustionCondition

```python
from astrosdk.domain.event_rules import CombustionCondition
from astrosdk.domain.combustion import CombustionState

condition = CombustionCondition(
    planet=Planet.MERCURY,
    states=[CombustionState.CAZIMI]  # Heart of the Sun
)
```

### SpeedCondition

```python
from astrosdk.domain.event_rules import SpeedCondition

condition = SpeedCondition(
    planet=Planet.MARS,
    operator="<",  # Less than
    value=0.5  # degrees per day
)
```

### RetrogradeCondition

```python
from astrosdk.domain.event_rules import RetrogradeCondition

condition = RetrogradeCondition(
    planet=Planet.JUPITER,
    is_retrograde=True
)
```

### LongitudeCondition

```python
from astrosdk.domain.event_rules import LongitudeCondition

condition = LongitudeCondition(
    planet=Planet.MOON,
    min_longitude=0.0,   # 0° Aries
    max_longitude=30.0   # 30° Aries (end of Aries)
)
```

## Combining Conditions

### AND Logic

```python
# Mercury retrograde AND in Gemini
rule = EventRule(
    name="Mercury Rx in Gemini",
    conditions=[
        RetrogradeCondition(planet=Planet.MERCURY, is_retrograde=True),
        LongitudeCondition(planet=Planet.MERCURY, min_longitude=60.0, max_longitude=90.0)
    ],
    logic=LogicOperator.AND
)
```

### OR Logic

```python
# Sun conjunct OR opposite Mars
rule = EventRule(
    name="Sun-Mars Hard Aspect",
    conditions=[
        AspectCondition(
            planet1=Planet.SUN,
            planet2=Planet.MARS,
            aspect_types=["CONJUNCTION"]
        ),
        AspectCondition(
            planet1=Planet.SUN,
            planet2=Planet.MARS,
            aspect_types=["OPPOSITION"]
        )
    ],
    logic=LogicOperator.OR
)
```

## Scanning Time Ranges

```python
from astrosdk.domain.event_rules import scan_time_range
from astrosdk import calculate_natal_chart, calculate_aspects, AstroTime
from datetime import datetime, timezone

# Define callback to get chart data
def get_chart_data(dt):
    time = AstroTime(dt)
    chart = calculate_natal_chart(time, 40.7, -74.0)
    aspects = calculate_aspects(chart.planets)
    return chart.planets, aspects

# Scan 2024
matches = scan_time_range(
    start_time=datetime(2024, 1, 1, tzinfo=timezone.utc),
    end_time=datetime(2024, 12, 31, tzinfo=timezone.utc),
    rules=[rule],
    interval_hours=24,
    get_chart_data_callback=get_chart_data
)

# Print matches
for match in matches:
    print(f"{match.rule_name} at {match.timestamp}")
    print(f"  Matched {match.matched_conditions}/{match.total_conditions} conditions")
```

## Complex Example

```python
# "Venus in dignity AND aspecting Jupiter"
complex_rule = EventRule(
    name="Venus-Jupiter Benefic Pattern",
    conditions=[
        DignityCondition(
            planet=Planet.VENUS,
            dignity_types=[
                DignityType.RULER,
                DignityType.EXALTATION
            ]
        ),
        AspectCondition(
            planet1=Planet.VENUS,
            planet2=Planet.JUPITER,
            aspect_types=["TRINE", "SEXTILE"],
            max_orb=6.0
        )
    ],
    logic=LogicOperator.AND
)
```

## Use Cases

### Market Timing
```python
# Detect Mars-Uranus squares (volatility indicator)
volatility_rule = EventRule(
    name="Volatility Spike",
    conditions=[
        AspectCondition(
            planet1=Planet.MARS,
            planet2=Planet.URANUS,
            aspect_types=["SQUARE"],
            max_orb=3.0
        )
    ],
    logic=LogicOperator.AND
)
```

### Electional Astrology
```python
# Find auspicious times: Moon not void, Venus dignified
election_rule = EventRule(
    name="Auspicious Election",
    conditions=[
        SpeedCondition(planet=Planet.MOON, operator=">", value=12.0),
        DignityCondition(
            planet=Planet.VENUS,
            dignity_types=[DignityType.RULER, DignityType.EXALTATION]
        )
    ],
    logic=LogicOperator.AND
)
```

## Performance Tips

1. **Use larger intervals** for long time ranges (24-48 hours)
2. **Narrow date ranges** when possible
3. **Combine related conditions** with AND logic
4. **Cache chart calculations** if scanning multiple rules

## See Also

- [API Reference](../api/public.md) - Event rule models
- [Aspects Guide](../guide/aspects.md) - Understanding aspects
