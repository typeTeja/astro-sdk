# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-02-16

### Added
- **Heliocentric Support**: Ability to calculate planetary positions from the Sun's center.
- **Planetary Crossings**:
  - Solar and Lunar Return detection with exact time calculation.
  - Planetary Sign Ingress detection (supporting both Tropical and Sidereal).
- **Nodes & Apsides**:
  - North/South Lunar Nodes (True and Mean).
  - Planetary Ascending/Descending Nodes.
  - Perihelion/Aphelion (Apsides) and Perigee/Apogee (Moon).
- **Horizon & Transits**:
  - `HorizonService` for precise Sunrise, Sunset, and Transit calculations.
  - Support for Civil, Nautical, and Astronomical twilight.
- **Heliacal Events**:
  - Heliacal Rising/Setting and Acronychal/Cosmical rising/setting.
  - Support for planets and fixed stars.
- **Horizontal Coordinates**: Added Azimuth, Altitude, and Zenith Distance to `PlanetPosition`.
- **Stations**: Detection of planetary Direct/Retrograde stations.
- **Parans & Antiscia**:
  - `ParanService` for simultaneous horizon/meridian crossing detection.
  - Automatic calculation of Antiscia and Contra-antiscia in `PlanetPosition`.
- **Tropical Support**: Updated `NatalService` to allow explicitly requested tropical calculations.

### Changed
- `NatalService.calculate_positions` now accepts `lat`, `lon`, and `alt` to automatically populate horizontal coordinates.
- Updated `PlanetPosition` domain model with 5 new properties (azimuth, altitude, zenith_distance, antiscia, contra_antiscia).

### Fixed
- Sidereal mode enforcement in `NatalService` fixed to allow tropical charts.
- Improved precision in orbital root-finding for crossings.

## [1.1.0] - 2026-02-16

### Added
- **47 ayanamsa systems** (expanded from 4 to 47)
  - Traditional: Fagan/Bradley, Lahiri, Raman, Krishnamurti, Sri Yukteshwar, etc.
  - Vedic/Hindu: Suryasiddhanta, Aryabhata, True Citra, True Revati, True Pushya
  - Babylonian: Kugler 1/2/3, Huber, ETPSC, Britton
  - Galactic: Galactic Center variants, Galactic Equator systems
  - Reference: J2000, J1900, B1950, Aldebaran at 15 Taurus
- **20 aspect types** (expanded from 5 to 20)
  - Major aspects (5): Conjunction, Sextile, Square, Trine, Opposition
  - Minor aspects (4): Semi-sextile, Semi-square, Sesqui-quadrate, Quincunx
  - Kepler aspects (2): Quintile, Biquintile
  - Septile family (3): Septile, Biseptile, Triseptile
  - Novile family (3): Novile, Binovile, Quadnovile
  - Undecile family (3): Undecile, Biundecile, Triundecile
- **Configurable aspect filtering** by type (major, minor, Kepler, septile, novile, undecile, all)
- **Custom orb configuration** per aspect type
- Comprehensive test suite for all new aspects and ayanamsas (17 new tests)

### Changed
- Enhanced `AspectService.calculate_aspects()` with `aspect_types` and `custom_orbs` parameters
- Updated default orbs: CONJUNCTION (8.0° → 10.0°), OPPOSITION (8.0° → 10.0°)
- Expanded `SiderealMode` enum with 43 additional ayanamsa systems

### Fixed
- Aspect orb boundary test updated for new CONJUNCTION orb (10.0°)

## [1.0.0] - 2026-02-15

### Added
- Comprehensive documentation (README, SECURITY policy)
- Type checking configuration (mypy)
- Code quality tools (ruff)
- Enhanced test coverage for edge cases
- CI/CD pipeline with GitHub Actions

### Fixed
- Applying/separating aspect detection logic
- Search range validation in eclipse calculations

## [0.1.0] - 2026-02-15

### Added
- Core ephemeris wrapper with thread safety (RLock)
- Deterministic time handling (UTC-only, no naive datetimes)
- Immutable domain models (Planet, Chart, Aspect, House, etc.)
- Service layer for natal charts, transits, aspects, events, cycles
- Engine layer for high-level orchestration
- Ephemeris context manager for state isolation
- Engine metadata exposure
- Comprehensive error hierarchy
- Planet validation against allowed list
- Performance guardrails (MAX_SEARCH_DAYS)
- Regression tests for enterprise determinism
- Support for multiple house systems
- Fixed star calculations
- Planetary phenomena calculations
- Eclipse search (solar and lunar)
- Sidereal and tropical zodiac support
- Multiple ayanamsa systems (Lahiri, Krishnamurti, Fagan-Bradley, Raman)

### Security
- No financial prediction or advice logic
- Input validation for planetary bodies
- Thread-safe global state management
- Structured exception handling

### Dependencies
- pyswisseph 2.10.3.2
- python-dotenv 1.0.1
- tzdata 2025.1

[Unreleased]: https://github.com/yourusername/astrosdk/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/astrosdk/releases/tag/v0.1.0
