# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-02-16

### Added - Phase 8: KP Houses & Domain Purity
- **KP (Krishnamurti Paddhati) House System**:
  - 27 Nakshatra (lunar mansion) calculations with planetary lords
  - Vimshottari sub-lord calculations using proportional dasha periods
  - 3-tier rulership: Sign Lord, Star Lord (Nakshatra), Sub-Lord
  - `calculate_kp_houses()` conversion from Placidus cusps
  - `KPCusp` and `KPHouseSystem` Pydantic models
- **Time Engine Hardening**: Fully deterministic time handling
  - No `datetime.now()` usage anywhere in codebase
  - Timezone enforcement via `Time` class
  - `AstroTime` public wrapper for user-facing API
  - Deterministic Julian Day calculations

### Added - Phase 9: Advanced Features
- **Custom Event Rule Engine** (`event_rules.py`):
  - JSON-driven pattern matching with 6 condition types:
    - `AspectCondition`: Planetary aspect detection
    - `DignityCondition`: Essential dignity matching
    - `CombustionCondition`: Combustion/cazimi/under beams
    - `SpeedCondition`: Speed comparisons (<, >, ==, <=, >=)
    - `RetrogradeCondition`: Retrograde motion detection
    - `LongitudeCondition`: Longitude range matching (with wraparound)
  - `EventRule` with AND/OR logic operators
  - `scan_time_range()` for event detection over date ranges
  - `RuleMatch` model with match percentages
- **Synodic Cycles** (`synodic.py`):
  - Phase angle calculation between planetary pairs
  - 8-phase cycle classification (conjunction, crescents, quarters, gibbous, opposition)
  - `SynodicCycle` and `SynodicPhase` models
- **Astro-Intensity Signals** (`intensity.py`):
  - Multi-factor 0-1 normalized activity scoring
  - Contributing factors: aspect density, retrograde count, station points, tight aspects
  - Activity level classification (quiet/moderate/active/extremely_active)
  - `IntensitySignal` model with driver analysis
- **Declination Parallels** (`declination.py`):
  - Parallel (same declination) aspect detection
  - Contra-parallel (opposite declination) detection
  - Out-of-ecliptic aspect support
  - `DeclinationAspect` model
- **Ephemeris Export** (`ephemeris_export.py`):
  - CSV export with complete planetary data
  - JSON export with structured time series
  - Configurable intervals for research/backtesting

### Added - Phase 10: Research Tools
- **Midpoints** (`midpoints.py`):
  - Direct midpoint calculations (near/far midpoints)
  - `MidpointTree` for sorted zodiacal ordering
  - Cluster detection for identifying sensitive degree areas
  - `find_midpoint_aspects()` for activation analysis
- **Harmonic Charts** (`harmonics.py`):
  - Harmonic longitude calculation (H2, H3, H5, H7, H9, H12, etc.)
  - Complete harmonic chart generation for any harmonic number
  - Harmonic aspect detection (focuses on conjunctions)
  - `HarmonicChart` and `HarmonicPosition` models
- **Primary Directions** (`primary_directions.py`):
  - Direct and converse arc calculations (1° = 1 year symbolic progression)
  - `DirectedPosition` model for all planets at any age
  - Firdaria time lord system (Medieval planetary periods)
  - Day/night birth differentiation
- **Astro-Cartography** (`astrocartography.py`):
  - Planetary line calculations (AS, MC, DS, IC)
  - `AstroMap` model with comprehensive line filtering
  - `Paran` model for simultaneous planetary angles
  - Location-based planetary activation analysis

### Changed - Architecture
- **Complete Pydantic v2 Migration**: All domain models now use Pydantic BaseModel
  - Immutable models with `frozen=True` configuration
  - Field validation with ge/le/lt constraints
  - Computed properties via `@computed_field`
  - Type safety throughout the codebase
- **Public Facade API**: Clean `__init__.py` exposing only essential functions
  - `calculate_natal_chart()`, `calculate_transit_chart()`, `calculate_synastry()`
  - `calculate_aspects()`, `find_planetary_aspects()`
  - Event-finding functions for eclipses, crossings, stations
  - `AstroTime` wrapper for time handling
- **Domain Purity**: All domain models are pure data with no external dependencies
  - No Swiss Ephemeris calls in domain layer
  - Services handle all ephemeris interactions
  - Clean separation of concerns

### Tests
- **177 total tests** (45 new tests in v1.3.0):
  - 22 KP House tests
  - 17 Event Rule Engine tests
  - 10 Advanced Features tests (synodic, intensity, declination, export)
  - 18 Research Tools tests (midpoints, harmonics, directions, astrocartography)
- All tests passing with 100% deter deterministic output

### Performance
- Maintained deterministic calculation guarantees
- Thread-safe ephemeris handling
- Efficient Pydantic model validation

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
  - Sept ile family (3): Septile, Biseptile, Triseptile
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

[Unreleased]: https://github.com/yourusername/astrosdk/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/yourusername/astrosdk/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/yourusername/astrosdk/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/yourusername/astrosdk/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yourusername/astrosdk/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/yourusername/astrosdk/releases/tag/v0.1.0
