# AstroSDK

**Production-Grade Astronomical Calculation Engine**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-177%20passing-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)]()

AstroSDK is a **deterministic, type-safe astronomical calculation engine** built on Swiss Ephemeris with Pydantic v2. Designed for research, data science, and applications requiring absolute precision and reproducibility.

---

## ✨ What's New in v1.3.0

### Complete Pydantic v2 Refactor
- **Immutable domain models** with full type safety
- **Clean public API** via facade pattern
- **Domain purity** - no Swiss Ephemeris in domain layer
- **Deterministic time** - no `datetime.now()` anywhere

### 45 New Features
- **KP House System** with Nakshatra and sub-lords
- **Event Rule Engine** with JSON-driven pattern matching
- **Synodic Cycles** with 8-phase classification
- **Astro-Intensity Signals** with multi-factor scoring
- **Midpoints & Harmonic Charts** (H2-H12+)
- **Primary Directions** with Firdaria time lords
- **Astro-Cartography** with planetary lines

[See CHANGELOG.md for full details](CHANGELOG.md)

---

## 🎯 Core Principles

- **Correctness over Speed** - Astronomical precision is never compromised
- **Determinism over Convenience** - Same input always produces identical output
- **Explicitness over Brevity** - No hidden defaults or assumptions
- **Type Safety** - Pydantic v2 models with full validation

---

## 🚀 Quick Start

### Installation

```bash
pip install astrosdk
```

### Basic Usage

```python
from astrosdk import calculate_natal_chart, AstroTime, Planet

# Create timezone-aware time
time = AstroTime.from_components(1990, 1, 1, 12, 0, tz="UTC")

# Calculate natal chart
chart = calculate_natal_chart(
    time=time,
    latitude=40.7128,   # New York City
    longitude=-74.0060,
    sidereal_mode=None  # None = Tropical, or use SiderealMode.LAHIRI
)

# Access planets (Pydantic models with validation)
for planet_pos in chart.planets:
    print(f"{planet_pos.planet.name}: {planet_pos.longitude:.2f}°")
    print(f"  {planet_pos.sign.name} {planet_pos.sign_degree:.2f}°")
    if planet_pos.is_retrograde:
        print(f"  ⟲ Retrograde (speed: {planet_pos.speed_long:.4f}°/day)")
```

### Calculate Aspects

```python
from astrosdk import calculate_aspects

# Major aspects only (default)
aspects = calculate_aspects(chart.planets)

# All aspect types
all_aspects = calculate_aspects(chart.planets, types=['all'])

# Specific types with custom orbs
aspects = calculate_aspects(
    chart.planets,
    types=['major', 'minor'],
    orbs={'CONJUNCTION': 12.0, 'SQUARE': 8.0}
)

for aspect in aspects:
    print(f"{aspect.p1.name} {aspect.type} {aspect.p2.name}")
    print(f"  Orb: {aspect.orb:.2f}° ({'applying' if aspect.applying else 'separating'})")
```

---

## 📚 Feature Showcase

### KP House System

```python
from astrosdk.domain.kp_houses import calculate_kp_houses

# Get Placidus cusps from chart
placidus_cusps = [cusp.longitude for cusp in chart.houses.cusps]

# Convert to KP system
kp_system = calculate_kp_houses(
    house_cusps=placidus_cusps,
    ascendant=chart.houses.axes.ascendant,
    midheaven=chart.houses.axes.midheaven
)

# Access 3-tier rulership
for cusp in kp_system.cusps:
    print(f"House {cusp.house_number}:")
    print(f"  Sign Lord: {cusp.sign_lord.name}")
    print(f"  Star Lord: {cusp.star_lord.name}")
    print(f"  Sub-Lord: {cusp.sub_lord.name}")
```

### Event Rule Engine

```python
from astrosdk.domain.event_rules import (
    EventRule, AspectCondition, RetrogradeCondition, LogicOperator
)
from datetime import datetime, timezone, timedelta

# Define rule: "Mercury retrograde AND aspecting Sun"
rule = EventRule(
    name="Mercury Rx + Sun Aspect",
    conditions=[
        RetrogradeCondition(planet=Planet.MERCURY, is_retrograde=True),
        AspectCondition(
            planet1=Planet.MERCURY,
            planet2=Planet.SUN,
            aspect_types=["CONJUNCTION", "OPPOSITION"]
        )
    ],
    logic=LogicOperator.AND
)

# Scan time range (requires callback to get chart data)
def get_chart_data(dt):
    time = AstroTime(dt)
    chart = calculate_natal_chart(time, 40.7, -74.0)
    aspects = calculate_aspects(chart.planets)
    return chart.planets, aspects

matches = scan_time_range(
    start_time=datetime(2024, 1, 1, tzinfo=timezone.utc),
    end_time=datetime(2024, 12, 31, tzinfo=timezone.utc),
    rules=[rule],
    interval_hours=24,
    get_chart_data_callback=get_chart_data
)

for match in matches:
    print(f"{match.rule_name} at {match.timestamp}")
```

### Harmonic Charts

```python
from astrosdk.domain.harmonics import calculate_harmonic_positions

# Generate 5th harmonic chart
h5 = calculate_harmonic_positions(chart.planets, harmonic=5)

# Check Sun in H5
sun_h5 = h5.get_planet(Planet.SUN)
print(f"Sun H5: {sun_h5.harmonic_longitude:.2f}° {sun_h5.sign.name}")

# Find harmonic conjunctions
from astrosdk.domain.harmonics import find_harmonic_aspects
h5_aspects = find_harmonic_aspects(h5, orb=2.0)

for p1, p2, orb in h5_aspects:
    print(f"{p1.name}-{p2.name} conjunction in H5: {orb:.2f}° orb")
```

### Midpoints

```python
from astrosdk.domain.midpoints import calculate_all_midpoints, find_midpoint_aspects

# Calculate all midpoints
midpoints = calculate_all_midpoints(chart.planets)

# Find Sun/Moon midpoint
sun_moon = [m for m in midpoints.midpoints 
            if {m.planet1, m.planet2} == {Planet.SUN, Planet.MOON}][0]

print(f"Sun/Moon midpoint: {sun_moon.midpoint_longitude:.2f}°")

# Find midpoints activated by a transit
transit_long = 150.0  # 0° Virgo
activated = find_midpoint_aspects(midpoints.midpoints, transit_long, orb=1.0)

for mp in activated:
    print(f"{mp.planet1.name}/{mp.planet2.name} activated")
```

### Primary Directions

```python
from astrosdk.domain.primary_directions import calculate_all_primary_directions

# Calculate directed positions at age 45
directed = calculate_all_primary_directions(chart.planets, age_years=45.0, method="direct")

for d in directed:
    print(f"{d.planet.name}:")
    print(f"  Natal: {d.natal_longitude:.1f}°")
    print(f"  Directed: {d.directed_longitude:.1f}°")
    print(f"  Arc: {d.arc_degrees:.1f}° ({d.age_years} years)")
```

### Astro-Cartography

```python
from astrosdk.domain.astrocartography import calculate_astromap

# Generate astro-cartography map
astro_map = calculate_astromap(chart.planets)

# Find where Jupiter is on MC
jupiter_mc_lines = [line for line in astro_map.lines
                    if line.planet == Planet.JUPITER and line.line_type == "MC"]

for line in jupiter_mc_lines:
    print(f"Jupiter MC line at {line.planet_longitude:.2f}°")
```

---

## 🔧 Advanced Features

### Combustion & Dignities

```python
from astrosdk.domain.combustion import check_combustion
from astrosdk.domain.dignity import calculate_dignity

# Check if Venus is combust
venus = next(p for p in chart.planets if p.planet == Planet.VENUS)
sun = next(p for p in chart.planets if p.planet == Planet.SUN)

combustion = check_combustion(venus.longitude, sun.longitude)
print(f"Venus combustion: {combustion.state.name}")  # COMBUST, CAZIMI, UNDER_BEAMS, or NONE

# Calculate essential dignity
dignity = calculate_dignity(
    planet=Planet.VENUS,
    sign=venus.sign,
    degree_in_sign=venus.sign_degree
)
print(f"Venus dignity: {dignity.type.name} (score: {dignity.score})")
```

### Planetary Acceleration

```python
from astrosdk import calculate_planet_acceleration

# Check if Mercury is near a station
accel = calculate_planet_acceleration(
    time=time,
    planet=Planet.MERCURY,
    time_delta_days=1.0
)

if accel.is_near_station:
    print(f"Mercury near station! Acceleration: {accel.longitude_accel:.6f}°/day²")
```

### Eclipses & Events

```python
from astrosdk import find_next_solar_eclipse, find_next_lunar_eclipse

# Find next solar eclipse
solar_eclipse = find_next_solar_eclipse(time)
if solar_eclipse:
    print(f"Next solar eclipse: {solar_eclipse.datetime}")

# Find next lunar eclipse
lunar_eclipse = find_next_lunar_eclipse(time)
if lunar_eclipse:
    print(f"Next lunar eclipse: {lunar_eclipse.datetime}")
```

### Sunrise & Sunset

```python
from astrosdk import calculate_sunrise_sunset

sun_times = calculate_sunrise_sunset(
    time=time,
    latitude=40.7128,
    longitude=-74.0060
)

print(f"Sunrise: {sun_times['sunrise'].datetime}")
print(f"Sunset: {sun_times['sunset'].datetime}")
```

---

## 🔄 Migration from v1.2.0

### Breaking Changes

1. **Pydantic v2 Models**: All domain models are now immutable Pydantic BaseModels
2. **Time Handling**: Use `AstroTime` wrapper instead of direct `Time` class
3. **Public API**: Use facade functions instead of direct service access

### Migration Example

```python
# OLD (v1.2.0)
from astrosdk.core.time import Time
from astrosdk.services.natal_service import NatalService
from astrosdk.core.ephemeris import Ephemeris

eph = Ephemeris()
service = NatalService(eph)
time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
chart = service.calculate_natal_chart(time, 40.7, -74.0, HouseSystem.PLACIDUS)

# NEW (v1.3.0)
from astrosdk import calculate_natal_chart, AstroTime

time = AstroTime.from_components(2000, 1, 1, 12, 0, tz="UTC")
chart = calculate_natal_chart(time=time, latitude=40.7, longitude=-74.0)
```

---

## 📖 Documentation

- **[Getting Started Guide](docs/getting-started.md)** - Installation and first steps
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Feature Guides](docs/features/)** - In-depth feature tutorials
- **[Migration Guide](docs/migration.md)** - Upgrading from v1.2.0
- **[CHANGELOG](CHANGELOG.md)** - Version history

---

## ⚠️ Important Disclaimers

### Financial Safety

> **This SDK provides astronomical data only. It does NOT:**
> - Predict prices or market movements
> - Provide financial advice or recommendations
> - Generate trading signals

Any financial application must implement its own interpretation layer and comply with applicable regulations.

### Deterministic Guarantee

AstroSDK guarantees deterministic output when:
- Same input parameters are provided
- Same Swiss Ephemeris version is used (2.10.3.2)
- Same ephemeris data files are present

Cross-platform determinism is maintained across Windows, Linux, and macOS.

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=astrosdk --cov-report=html

# Run specific test file
pytest tests/test_research_tools.py -v
```

**Current Status**: 177/177 tests passing ✅

---

## 📦 Dependencies

- **pyswisseph** 2.10.3.2 - Swiss Ephemeris calculations
- **pydantic** ≥2.0 - Data validation and models
- **python-dotenv** 1.0.1 - Environment configuration
- **tzdata** 2025.1 - Timezone data

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Swiss Ephemeris** by Astrodienst AG
- **Pydantic** for excellent data validation
- The astrological research community

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/astrosdk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/astrosdk/discussions)
- **Email**: support@astrosdk.dev

---

**Built with ❤️ for astronomical precision**
