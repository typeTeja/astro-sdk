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
Calculate a complete natal chart with planetary positions and house cusps.

**Features:**
- Timezone-aware time handling
- Planetary positions with retrograde detection
- House cusp calculations
- Angle calculations (ASC, MC, DESC, IC)

### 02_aspects.py
Calculate aspects between planets and identify applying/separating aspects.

**Features:**
- Major aspects (conjunction, opposition, trine, square, sextile)
- Orb calculations
- Applying vs separating detection
- Aspect summary statistics

### 03_eclipses.py
Search for solar and lunar eclipses within a time range.

**Features:**
- Solar eclipse search
- Lunar eclipse search
- Eclipse type detection (total, partial, annular)
- Search range validation

## More Examples

For more advanced usage, see:
- [README.md](../README.md) - Quick start guide
- [tests/](../tests/) - Test files showing various use cases
- Documentation (coming soon)

## Need Help?

- Check the [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for questions
- Read the source code - it's designed to be readable!
