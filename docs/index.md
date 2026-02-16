# AstroSDK Documentation

**Production-Grade Astronomical Calculation Engine**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-177%20passing-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)]()

---

## Welcome

AstroSDK is a **deterministic, type-safe astronomical calculation engine** built on Swiss Ephemeris with Pydantic v2. Designed for research, data science, and applications requiring absolute precision and reproducibility.

## Key Features

### ✨ v1.3.0 Highlights

- **Complete Pydantic v2 Refactor** - Immutable, validated domain models
- **Clean Public API** - User-friendly facade pattern
- **45 New Features** - KP Houses, Event Rules, Research Tools
- **177 Tests Passing** - 100% deterministic output
- **Domain Purity** - Clean architecture with no Swiss Ephemeris in domain layer

### Core Capabilities

- **Natal Charts** - Complete chart calculations with houses and planets
- **Aspects** - 20 aspect types (major, minor, Kepler, septile, novile, undecile)
- **47 Ayanamsas** - Comprehensive sidereal system support
- **Time Precision** - Deterministic, timezone-aware calculations
- **Events** - Eclipses, returns, crossings, stations
- **Research Tools** - Midpoints, harmonics, directions, astro-cartography

## Quick Example

```python
from astrosdk import calculate_natal_chart, AstroTime

# Create time
time = AstroTime.from_components(1990, 1, 1, 12, 0, tz="UTC")

# Calculate chart
chart = calculate_natal_chart(
    time=time,
    latitude=40.7128,
    longitude=-74.0060
)

# Access planets
for planet in chart.planets:
    print(f"{planet.planet.name}: {planet.longitude:.2f}°")
```

## Getting Started

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Quick Start__

    ---

    Get up and running in minutes

    [:octicons-arrow-right-24: Quick Start](getting-started/quick-start.md)

-   :material-book-open-variant:{ .lg .middle } __User Guide__

    ---

    Learn core concepts and features

    [:octicons-arrow-right-24: User Guide](guide/natal-charts.md)

-   :material-star:{ .lg .middle } __Advanced Features__

    ---

    Explore KP Houses, Event Rules, and more

    [:octicons-arrow-right-24: Features](features/kp-houses.md)

-   :material-code-braces:{ .lg .middle } __API Reference__

    ---

    Complete API documentation

    [:octicons-arrow-right-24: API Docs](api/public.md)

</div>

## Core Principles

!!! info "Design Philosophy"
    - **Correctness over Speed** - Astronomical precision is never compromised
    - **Determinism over Convenience** - Same input always produces identical output
    - **Explicitness over Brevity** - No hidden defaults or assumptions
    - **Type Safety** - Pydantic v2 models with full validation

## What's New in v1.3.0

### Architecture
- Complete Pydantic v2 migration for all domain models
- Public facade API with clean `__init__.py`
- Domain purity - no Swiss Ephemeris in domain layer
- Deterministic time handling - no `datetime.now()`

### New Features
- **KP House System** with Nakshatra and sub-lords (22 tests)
- **Event Rule Engine** with JSON-driven pattern matching (17 tests)
- **Synodic Cycles** with 8-phase classification
- **Astro-Intensity Signals** with multi-factor scoring
- **Midpoints & Harmonic Charts** (H2-H12+)
- **Primary Directions** with Firdaria time lords
- **Astro-Cartography** with planetary lines

[See full changelog →](about/changelog.md)

## Installation

```bash
pip install astrosdk
```

## Support

- **Documentation**: [astrosdk.dev](https://astrosdk.dev)
- **Issues**: [GitHub Issues](https://github.com/yourusername/astrosdk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/astrosdk/discussions)

---

**Built with ❤️ for astronomical precision**
