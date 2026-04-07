# AstroSDK Examples

This directory contains example scripts demonstrating how to use AstroSDK.

## Running Examples

Make sure you have installed AstroSDK:

```bash
pip install -e .
```

Set the ephemeris path (if not using default):

```bash
export SE_EPHE_PATH=/path/to/ephemeris/data
```

Run any example:

```bash
python examples/01_natal_chart.py
```

## Available Examples

### 01_natal_chart.py
Calculate a complete natal chart with planetary positions and house cusps using the high-level `ChartEngine`.

**Features:**
- Timezone-aware time handling
- Planetary positions with retrograde detection
- Horizontal coordinates (Azimuth/Altitude)
- House cusp and angle calculations (ASC, MC, DESC, IC)

### 02_aspects.py
Calculate aspects between planets and identify applying/separating aspects using the 20-aspect family filtering API.

**Features:**
- Major, Minor, and Kepler aspects
- Septile, Novile, and Undecile families
- Custom orb configuration
- Applying vs separating detection

### 02_advanced_features.py
Professional-grade features for research and precise astronomical scanning.

**Features:**
- Precise Horizon Events (Sunrise, Subset, Solar Noon)
- Heliacal Phenemona (Risings/Settings)
- Yearly Planetary Stations (Retrograde/Direct points)
- Simultaneous Events (Parans)
- Sign Ingresses (Exact 30° degree boundaries)

### 03_eclipses.py
Search for solar and lunar eclipses globally using high-precision Swiss Ephemeris models.

**Features:**
- Solar eclipse search
- Lunar eclipse search
- Magnitude and peak time results
- Total/Annular/Partial detection

## More Examples

For more advanced usage, see:
- [README.md](../README.md) - Quick start guide
- [tests/](../tests/) - Standard tests showing various use cases
- [src/app/engine/chart_engine.py](../src/app/engine/chart_engine.py) - For orchestration logic
- [src/app/services/](../src/app/services/) - For service implementation details

## Need Help?

- Check the [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for questions
- Read the source code - it's designed to be readable!
