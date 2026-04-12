# Changelog

All notable changes to the AstroSDK 2.0 Platform.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-04-12

### Added
- **API v2 Migration**: Moved the entire API surface from `/api/v1/` to `/api/v2/`.
- **Pure 2.0 Service Layer**: All external endpoints now utilize namespaced Services and `CalculationContext`.
- **Namespaced Domains**: Transitioned to modular domains (`astronomy`, `western`, `vedic`, `mundane`, `research`).
- **Research Enhancements**: New `ResearchFinancialService` and `ResearchQuantService` support high-precision signal scanning, intensity, and clustering.
- **Astronomy Graduation**: Native 2.0 services for `Parans`, `Fixed Stars`, `Nodes`, `Synodics`, and `Heliacal` events.
- **Context-First Architecture**: All calculations include a context fingerprint for auditability.

### Removed
- **Legacy Purge**: Deleted 25+ flat service files from `app/services/` and the original `ChartEngine`.
- **Legacy Domain models**: Purged orphaned models in `app/domain/` to avoid architectural confusion.
- **Phase-based Adapters**: Removed all `test_phase0` and `test_phase1` specific artifacts.

### Security
- Added mandatory `no_financial_advice: true` meta-block for consistency across financial research outputs.
