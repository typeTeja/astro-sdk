# AstroSDK 2.0 Phased Checklist

This checklist translates the AstroSDK 2.0 roadmap and GitHub backlog into a
repo-local execution plan. It is meant to be updated during implementation.

## How To Use This Checklist

- Mark tasks complete as work lands.
- Keep this file aligned with GitHub issues and milestones.
- If scope changes, update both this checklist and the backlog manifest.
- New AstroSDK 2.0 work should prefer the grouped 2.0 structure over the old flat layout.

## Phase 0: Architecture Baseline

Goal:
Establish the AstroSDK 2.0 architectural spine without breaking the current app.

- [x] Create `app/contexts/`
- [x] Add `CalculationContext`
- [x] Add `ZodiacContext`
- [x] Add `CoordinateContext`
- [x] Add `ObserverContext`
- [x] Add `HouseContext`
- [x] Add `FeatureContext`
- [x] Create grouped domain namespaces under `app/domain/`
- [x] Create grouped service namespaces under `app/services/`
- [x] Add capability registry in core platform code
- [x] Add `FeatureMaturity` enum
- [x] Add migration rules for old flat modules
- [x] Document placement rules for all new 2.0 features

Exit criteria:

- [x] New 2.0 architectural spine exists
- [x] Current tests still pass
- [x] New features can be added to the 2.0 layout immediately

Phase 0 status notes:

- [x] `v1` chart generation now runs through `CalculationContext` and `WesternChartService`
- [x] `ChartEngine` now delegates through the 2.0 Western chart service path
- [x] `v1` transit scanning now runs through `WesternTransitService`
- [x] `v1` aspect calculation now runs through `WesternAspectService`
- [x] Scaffold and migration path are covered by dedicated Phase 0 tests

## Phase 1: Core Determinism Hardening

Goal:
Make core calculations explicit, auditable, and safe.

- [ ] Centralize Swiss Ephemeris state mutation behind one runtime boundary
- [x] Audit all `swe.*` call sites for lock and state safety
- [ ] Move context-sensitive logic away from hidden flags
- [ ] Refactor new and migrated services to accept explicit context objects
- [x] Add calculation fingerprinting
- [x] Add engine version and context metadata for reproducibility
- [ ] Add tropical vs sidereal parity tests
- [ ] Add geocentric vs heliocentric parity tests
- [ ] Add topocentric coverage tests
- [ ] Add nested context regression tests

Exit criteria:

- [ ] Core mode handling is explicit
- [ ] State safety is centralized
- [x] Deterministic metadata is attached to calculations

Phase 1 status notes:

- [x] Context-backed Western chart, aspect, and transit paths now emit deterministic calculation fingerprints
- [x] Secondary progression calculation now runs through a context-backed Western progression adapter
- [x] Planetary return calculation now runs through a context-backed Western return adapter
- [x] `AstroMeta` now supports capability, feature maturity, calculation fingerprint, and engine version
- [x] Reproducibility metadata is covered by dedicated tests and verified in the full test suite
- [x] Runtime metadata now reads through the shared Swiss Ephemeris boundary
- [x] Nested sidereal-mode restoration is covered by tests
- [x] Topocentric state restoration is covered by tests
- [x] Tropical and sidereal isolation/parity behavior is covered by Phase 1 tests
- [x] Crossing and event services now scope sidereal/topocentric state with `EphemerisContext`

## Phase 2: Western Core 2.0

Goal:
Move core Western astrology features onto the 2.0 architecture.

- [ ] Create `app/services/western/chart_service.py`
- [ ] Create `app/services/western/transit_service.py`
- [ ] Create `app/services/western/aspect_service.py`
- [ ] Create `app/services/western/return_service.py`
- [ ] Add `TransitWindow` domain object
- [ ] Add `ReturnChart` domain object
- [ ] Add exact-time return support
- [ ] Add exact-time transit window support
- [ ] Add `SynastryAspect` domain object
- [ ] Add `CompositeChart` domain object
- [ ] Design `api/v2/western`
- [ ] Define maturity level for each Western feature

Exit criteria:

- [ ] Natal, transits, aspects, and returns work through the 2.0 service layer
- [ ] Western domain objects are richer than API schemas
- [ ] `api/v2/western` contract is ready

## Phase 3: Vedic Core 2.0

Goal:
Turn Vedic support into a structured subsystem with explicit domain models.

- [ ] Add `NakshatraPosition`
- [ ] Add `PadaPosition`
- [ ] Add `DashaPeriod`
- [ ] Add `VargaChart`
- [ ] Add `YogaHit`
- [ ] Add `AshtakavargaMatrix`
- [ ] Add `ShadbalaScore`
- [ ] Create `app/services/vedic/nakshatra_service.py`
- [ ] Create `app/services/vedic/dasha_service.py`
- [ ] Create `app/services/vedic/varga_service.py`
- [ ] Create `app/services/vedic/yoga_service.py`
- [ ] Create `app/services/vedic/ashtakavarga_service.py`
- [ ] Create `app/services/vedic/shadbala_service.py`
- [ ] Add Vimshottari dasha validation fixtures
- [ ] Add varga validation fixtures
- [ ] Define maturity level for advanced Vedic features
- [ ] Design `api/v2/vedic`

Exit criteria:

- [ ] Vedic features run through a domain-first subsystem
- [ ] Advanced Vedic outputs have explicit maturity markers
- [ ] `api/v2/vedic` contract is ready

## Phase 4: Mundane and Event Engine

Goal:
Create a durable subsystem for ingresses, stations, eclipses, and macro event scanning.

- [ ] Add `MundaneIngress`
- [ ] Add `StationEvent`
- [ ] Add `EventCluster`
- [ ] Create `app/services/mundane/ingress_service.py`
- [ ] Create `app/services/mundane/station_service.py`
- [ ] Create `app/services/mundane/event_service.py`
- [ ] Group ingress logic under the mundane subsystem
- [ ] Group station logic under the mundane subsystem
- [ ] Group eclipse and macro event logic under the mundane subsystem
- [ ] Add historical ingress fixtures
- [ ] Add historical station fixtures
- [ ] Add eclipse validation fixtures
- [ ] Define event scan tolerances in context models
- [ ] Move large event scans toward background job execution

Exit criteria:

- [ ] Event logic is grouped and scalable
- [ ] Historical event validation exists
- [ ] Long scans are no longer tied only to request-time paths

## Phase 5: Research Platform

Goal:
Support serious research and export workflows as first-class platform capabilities.

- [ ] Add `ResearchSeries`
- [ ] Add `DatasetExport`
- [ ] Add `MarketCycleCorrelation`
- [ ] Create `app/services/research/export_service.py`
- [ ] Create `app/services/research/scan_service.py`
- [ ] Create `app/services/research/statistics_service.py`
- [ ] Add export worker
- [ ] Add scan worker
- [ ] Add job state tracking for research operations
- [ ] Define CSV export contracts
- [ ] Define JSON export contracts
- [ ] Add reproducibility metadata to exported datasets
- [ ] Add capability reporting for research features

Exit criteria:

- [ ] Large research tasks can run asynchronously
- [ ] Dataset outputs are reproducible and versioned
- [ ] Research features are discoverable and maturity-tagged

## Phase 6: Alerts, Jobs, and Persistence

Goal:
Support durable workflows for alerts, saved charts, presets, and background jobs.

- [ ] Add persistence model for jobs
- [ ] Add persistence model for saved charts
- [ ] Add persistence model for user presets
- [ ] Separate alert rule management from alert scanning
- [ ] Create `app/services/alerts/alert_rule_service.py`
- [ ] Create `app/services/alerts/alert_scan_service.py`
- [ ] Create `app/services/alerts/notification_service.py`
- [ ] Add execution history for background scans
- [ ] Add execution history for alerts
- [ ] Add audit trails for workflow jobs
- [ ] Design notification adapter boundaries for webhook/email/app delivery

Exit criteria:

- [ ] Workflow entities persist cleanly
- [ ] Alerts and jobs scale independently
- [ ] Operational history is inspectable

## Phase 7: Public Surface Consolidation

Goal:
Make AstroSDK usable as a broader platform across API and SDK consumers.

- [ ] Create `api/v2/astronomy`
- [ ] Create `api/v2/western`
- [ ] Create `api/v2/vedic`
- [ ] Create `api/v2/mundane`
- [ ] Create `api/v2/research`
- [ ] Create `api/v2/alerts`
- [ ] Create `app/sdk/client.py`
- [ ] Create grouped SDK modules for Western, Vedic, and research usage
- [ ] Document capability registry usage
- [ ] Document maturity levels and compatibility policy
- [ ] Add examples for web backend usage
- [ ] Add examples for mobile-backend usage
- [ ] Add examples for desktop-backend usage
- [ ] Add examples for research/notebook usage

Exit criteria:

- [ ] `api/v2` is aligned to architecture domains
- [ ] Python SDK surface exists
- [ ] Public compatibility expectations are documented

## Cross-Phase Quality Gates

These should remain active throughout the AstroSDK 2.0 rollout.

- [ ] No new feature lands only in the old flat service layout
- [ ] No new core calculation depends on hidden mode defaults
- [ ] Experimental features are clearly marked
- [ ] API responses include reproducibility metadata where applicable
- [ ] Golden validation fixtures grow with feature coverage
- [ ] Heavy scans move to worker-backed execution when needed
- [ ] GitHub backlog stays aligned with implementation progress

## Suggested Working Order

1. Finish Phase 0 before introducing major new subsystems.
2. Prioritize Phase 1 before broadening public APIs further.
3. Build Western and Vedic 2.0 in parallel only after core context rules are stable.
4. Move large scan/export work into workers before research growth accelerates.
5. Treat public API and SDK consolidation as the final shaping pass, not the first one.
