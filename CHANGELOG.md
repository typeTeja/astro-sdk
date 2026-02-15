# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
