# AstroSDK

**Deterministic Astronomy & Astrology Calculation Engine**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AstroSDK is a production-grade, deterministic astronomical calculation engine built on Swiss Ephemeris. Designed for research, data science, and financial time-intelligence systems requiring absolute precision and reproducibility.

---

## 🎯 Core Principles

**This SDK is infrastructure, not an application.**

- **Correctness over Speed** - Astronomical precision is never compromised
- **Determinism over Convenience** - Same input always produces identical output
- **Explicitness over Brevity** - No hidden defaults or assumptions
- **Auditability over Abstraction** - Every calculation is traceable

---

## ⚠️ Important Disclaimers

### Financial Safety

> **This SDK provides astronomical data only. It does NOT:**
> - Predict prices or market movements
> - Provide financial advice or recommendations
> - Generate trading signals
> - Estimate volatility or risk

Any financial application must implement its own interpretation layer and comply with applicable regulations.

### Deterministic Guarantee

AstroSDK guarantees deterministic output when:
- Same input parameters are provided
- Same Swiss Ephemeris version is used
- Same ephemeris data files are present

Cross-platform determinism is maintained across Windows, Linux, and macOS.

---

## 🚀 Quick Start

### Installation

```bash
pip install astrosdk
```

### Basic Usage

```python
from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet, HouseSystem
from astrosdk.services.natal_service import NatalService

# Initialize ephemeris
eph = Ephemeris()

# Create a deterministic time (timezone-aware required)
birth_time = Time(datetime(1990, 1, 1, 12, 0, 0, tzinfo=timezone.utc))

# Calculate natal chart
natal_service = NatalService(eph)
chart = natal_service.calculate_natal_chart(
    time=birth_time,
    latitude=40.7128,
    longitude=-74.0060,
    house_system=HouseSystem.PLACIDUS
)

# Access planetary positions
for planet_pos in chart.planets:
    print(f"{planet_pos.planet.name}: {planet_pos.longitude:.4f}° "
          f"({planet_pos.sign.name} {planet_pos.sign_degree:.2f}°)")
    if planet_pos.is_retrograde:
        print(f"  ⟲ Retrograde")
```

### Calculate Aspects

```python
from astrosdk.services.aspect_service import AspectService

aspect_service = AspectService()

# Major aspects only (default)
aspects = aspect_service.calculate_aspects(chart.planets)

# All aspect types (major, minor, Kepler, septile, novile, undecile)
all_aspects = aspect_service.calculate_aspects(chart.planets, aspect_types=['all'])

# Specific aspect types
combined = aspect_service.calculate_aspects(chart.planets, aspect_types=['major', 'minor'])

# Custom orbs
custom_aspects = aspect_service.calculate_aspects(
    chart.planets,
    aspect_types=['major'],
    custom_orbs={"CONJUNCTION": 15.0, "TRINE": 12.0}
)

for aspect in aspects:
    print(f"{aspect.p1.name} {aspect.type} {aspect.p2.name} "
          f"(orb: {aspect.orb:.2f}°, {'applying' if aspect.applying else 'separating'})")
```

### Find Eclipses

```python
from astrosdk.services.event_service import EventService

event_service = EventService(eph)
next_eclipse = event_service.find_next_solar_eclipse(birth_time)

print(f"Next solar eclipse: JD {next_eclipse.peak_jd}")
print(f"Type: {next_eclipse.type}")
```

---

## 📐 Architecture

```
astrosdk/
├── core/           # Swiss Ephemeris wrapper, time handling, constants
├── domain/         # Immutable data models (Planet, Chart, Aspect, etc.)
├── services/       # Business logic (natal, transit, aspect calculations)
└── engine/         # High-level orchestration and metadata
```

### Design Philosophy

- **Core Layer**: Thread-safe Swiss Ephemeris access, deterministic time conversion
- **Domain Layer**: Immutable frozen dataclasses, no business logic
- **Service Layer**: Pure functions, no side effects, no I/O
- **Engine Layer**: Multi-service coordination, batch processing

---

## 🔧 Configuration

### Ephemeris Path

Set the ephemeris data path via environment variable:

```bash
export SE_EPHE_PATH=/usr/share/libswe/ephe
```

Or create a `.env` file:

```
SE_EPHE_PATH=/path/to/ephemeris/data
```

### Sidereal Mode

Default: **Lahiri** (Sidereal)

AstroSDK supports **47 ayanamsa systems** from Swiss Ephemeris:

**Traditional Systems:**
- `FAGAN_BRADLEY` - Western sidereal
- `LAHIRI` - Indian government standard
- `RAMAN` - B.V. Raman
- `KRISHNAMURTI` - KP system
- `YUKTESHWAR` - Sri Yukteshwar
- And 42 more including Vedic, Babylonian, Galactic, and reference systems

```python
from astrosdk.core.constants import SiderealMode

# Lahiri (default)
eph.set_sidereal_mode(SiderealMode.LAHIRI)

# Krishnamurti (KP)
eph.set_sidereal_mode(SiderealMode.KRISHNAMURTI)

# Fagan/Bradley (Western sidereal)
eph.set_sidereal_mode(SiderealMode.FAGAN_BRADLEY)

# Galactic Center at 0 Sagittarius
eph.set_sidereal_mode(SiderealMode.GALCENT_0SAG)

# J2000 reference
eph.set_sidereal_mode(SiderealMode.J2000)
```

See `SiderealMode` enum for all 47 systems.

### House Systems

Supported systems:
- Placidus (default)
- Koch
- Whole Sign
- Equal
- Porphyry
- Regiomontanus
- Campanus
- Vedic (Equal from Ascendant)

---

## 🧪 Testing & Reliability

AstroSDK includes comprehensive regression tests:

```bash
pytest tests/ -v
```

### Determinism Verification

```python
from astrosdk.engine.metadata import get_engine_metadata

metadata = get_engine_metadata()
print(metadata)
# {
#   'pyswisseph_version': '2.10.03.02',
#   'de_number': 431,
#   'tidal_acceleration': -25.8,
#   'sidereal_default': 'LAHIRI',
#   ...
# }
```

---

## 🔒 Thread Safety

All Swiss Ephemeris calls are protected by a global `RLock`. AstroSDK is safe for:
- Multi-threaded applications
- Async/await contexts
- Concurrent request handling

---

## 📊 Supported Calculations

### Planetary Positions
- Longitude, latitude, distance
- Speed (daily motion)
- Retrograde detection and Station dates
- Zodiac sign and degree (Antiscia/Contra-antiscia)
- Local Azimuth/Altitude/Zenith Distance

### Aspects

**20 Aspect Types** organized by harmonic families:

**Major Aspects (Ptolemaic):**
- Conjunction (0°), Sextile (60°), Square (90°), Trine (120°), Opposition (180°)

**Minor Aspects:**
- Semi-sextile (30°), Semi-square (45°), Sesqui-quadrate (135°), Quincunx (150°)

**Kepler Aspects (Quintile family):**
- Quintile (72°), Biquintile (144°)

**Septile Family (7th harmonic):**
- Septile (51.43°), Biseptile (102.86°), Triseptile (154.29°)

**Novile Family (9th harmonic):**
- Novile (40°), Binovile (80°), Quadnovile (160°)

**Undecile Family (11th harmonic):**
- Undecile (32.73°), Biundecile (65.45°), Triundecile (98.18°)

**Features:**
- Configurable orbs per aspect
- Aspect type filtering (major, minor, Kepler, etc.)
- Applying/separating detection
- Geocentric and heliocentric
- Sidereal and tropical
- Multiple ayanamsa systems (47 supported)

### Locational Astronomy (Horizon)

**Horizon Events:**
- Sunrise, Sunset, Moonrise, Moonset
- Transits (Culminations) and Anticulminations (IC)
- All twilight types: Civil, Nautical, Astronomical
- Accounts for atmospheric refraction and observer altitude

**Horizontal Coordinates:**
- Real-time Azimuth, Altitude, and Zenith Distance
- Automated conversion from equatorial/ecliptic to local horizontal

### Specialized Celestial Events

**Heliacal Phenomena:**
- Heliacal Risings (First Visibility) and Settings (Last Visibility)
- Acronychal Risings and Cosmical Settings
- Support for planets and fixed stars

**Planetary Stations:**
- Precise detection of Direct and Retrograde station dates
- Orbital speed zero-crossing analysis

**Simultaneous Events (Parans):**
- Simultaneous horizon/meridian crossings for any location
- Parans between planets and fixed stars

### Planetary Dynamics

**Nodes & Apsides:**
- North/South Lunar Nodes (True and Mean)
- Planetary Ascending/Descending Nodes
- Perihelion/Aphelion (Apsides) for all bodies
- Perigee/Apogee for the Moon

**Crossings & Cycles:**
- Solar and Lunar Returns
- Planetary Sign Ingresses (Tropical and Sidereal)
- Exact time calculation for returns and ingresses

### Fixed Stars
- Position calculation
- Magnitude data
- Conjunction detection

### Houses
- 12 house cusps
- Ascendant, Midheaven, Vertex
- Multiple house systems

### Aspects
- Conjunction, Opposition, Square, Trine, Sextile
- Configurable orbs
- Applying/separating detection

### Events
- Solar and lunar eclipses
- Planetary ingresses (sign changes)
- Rise/set/transit times

### Phenomena
- Phase angle and illumination
- Elongation from Sun
- Apparent magnitude
- Apparent diameter

---

## 🚫 What This SDK Does NOT Do

- ❌ Interpretation or predictions
- ❌ Machine learning or AI
- ❌ HTTP APIs or web services
- ❌ Database operations
- ❌ UI rendering
- ❌ Financial advice or signals

---

## 📚 Advanced Usage

### Context Isolation

For temporary state changes:

```python
from astrosdk.core.ephemeris_context import EphemerisContext
from astrosdk.core.constants import SiderealMode

with EphemerisContext(sid_mode=SiderealMode.FAGAN_BRADLEY):
    # Calculations here use Fagan-Bradley
    position = eph.calculate_planet(jd, Planet.MARS)

# Automatically restored to Lahiri
```

### Topocentric Calculations

```python
eph.set_topocentric(
    lat=40.7128,
    lon=-74.0060,
    alt=10.0  # meters above sea level
)
```

---

## 🛠️ Development

### Requirements

- Python 3.11+
- pyswisseph 2.10.3.2
- Swiss Ephemeris data files

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[test]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/astrosdk --cov-report=term-missing
```

---

## 📖 Documentation

- [Architecture Philosophy](./docs/architecture.md) *(coming soon)*
- [API Reference](./docs/api.md) *(coming soon)*
- [Examples](./examples/) *(coming soon)*

---

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. All tests pass
2. Type hints are complete
3. Docstrings follow NumPy style
4. No breaking changes without major version bump

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

---

## 🔗 Resources

- [Swiss Ephemeris](https://www.astro.com/swisseph/)
- [pyswisseph Documentation](https://astrorigin.com/pyswisseph/)

---

## ⚖️ Regulatory Compliance

This SDK is designed for:
- Research and academic use
- Data science applications
- Time-intelligence systems
- Astronomical calculations

**Users are responsible for ensuring compliance with applicable financial regulations in their jurisdiction.**

---

**Built with precision. Designed for longevity. Optimized for correctness.**
