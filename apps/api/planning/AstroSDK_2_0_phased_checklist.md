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

## Phase 1: Core Determinism Hardening

Goal:
Make core calculations explicit, auditable, and safe.

- [x] Centralize Swiss Ephemeris state mutation behind one runtime boundary
- [x] Audit all `swe.*` call sites for lock and state safety
- [x] Move context-sensitive logic away from hidden flags
- [x] Refactor new and migrated services to accept explicit context objects
- [x] Add calculation fingerprinting
- [x] Add engine version and context metadata for reproducibility
- [x] Add tropical vs sidereal parity tests
- [x] Add geocentric vs heliocentric parity tests
- [x] Add topocentric coverage tests
- [x] Add nested context regression tests

Exit criteria:

- [x] Core mode handling is explicit
- [x] State safety is centralized
- [x] Deterministic metadata is attached to calculations

## Phase 2: Western Core 2.0

Goal:
Move core Western astrology features onto the 2.0 architecture.

- [x] Create `app/services/western/chart_service.py`
- [x] Create `app/services/western/transit_service.py`
- [x] Create `app/services/western/aspect_service.py`
- [x] Create `app/services/western/return_service.py`
- [x] Add `TransitWindow` domain object
- [x] Add `ReturnChart` domain object
- [x] Add exact-time return support
- [x] Add exact-time transit window support
- [x] Add `SynastryAspect` domain object
- [x] Add `CompositeChart` domain object
- [x] Design `api/v2/western`
- [x] Define maturity level for each Western feature

Exit criteria:

- [x] Natal, transits, aspects, and returns work through the 2.0 service layer
- [x] Western domain objects are richer than API schemas
- [x] `api/v2/western` contract is ready

## Phase 3: Vedic Core 2.0

Goal:
Turn Vedic support into a structured subsystem with explicit domain models.

- [x] Add `NakshatraPosition`
- [x] Add `PadaPosition`
- [x] Add `DashaPeriod`
- [x] Add `VargaChart`
- [x] Add `YogaHit`
- [x] Add `AshtakavargaMatrix`
- [x] Add `ShadbalaScore`
- [x] Create `app/services/vedic/nakshatra_service.py`
- [x] Create `app/services/vedic/dasha_service.py`
- [x] Create `app/services/vedic/varga_service.py`
- [x] Create `app/services/vedic/yoga_service.py`
- [x] Create `app/services/vedic/ashtakavarga_service.py`
- [x] Create `app/services/vedic/shadbala_service.py`
- [x] Add Vimshottari dasha validation fixtures
- [x] Add varga validation fixtures
- [x] Define maturity level for advanced Vedic features
- [x] Design `api/v2/vedic`

Exit criteria:

- [x] Vedic features run through a domain-first subsystem
- [x] Advanced Vedic outputs have explicit maturity markers
- [x] `api/v2/vedic` contract is ready

## Phase 4: Mundane and Event Engine

Goal:
Create a durable subsystem for ingresses, stations, eclipses, and macro event scanning.

- [x] Add `MundaneIngress`
- [x] Add `StationEvent`
- [x] Add `EventCluster`
- [x] Create `app/services/mundane/ingress_service.py`
- [x] Create `app/services/mundane/station_service.py`
- [x] Create `app/services/mundane/event_service.py`
- [x] Group ingress logic under the mundane subsystem
- [x] Group station logic under the mundane subsystem
- [x] Group eclipse and macro event logic under the mundane subsystem
- [x] Add historical ingress fixtures
- [x] Add historical station fixtures
- [x] Add eclipse validation fixtures
- [x] Define event scan tolerances in context models
- [x] Move large event scans toward background job execution

Exit criteria:

- [x] Event logic is grouped and scalable
- [x] Historical event validation exists
- [x] Long scans are no longer tied only to request-time paths

## Phase 5: Research Platform

Goal:
Support serious research and export workflows as first-class platform capabilities.

- [x] Add `ResearchSeries`
- [x] Add `DatasetExport`
- [x] Add `MarketCycleCorrelation`
- [x] Create `app/services/research/export_service.py`
- [x] Create `app/services/research/statistics_service.py`
- [x] Add export worker
- [x] Add scan worker
- [x] Add job state tracking for research operations
- [x] Define CSV export contracts
- [x] Define JSON export contracts
- [x] Add reproducibility metadata to exported datasets
- [x] Add capability reporting for research features

Exit criteria:

- [x] Large research tasks can run asynchronously
- [x] Dataset outputs are reproducible and versioned
- [x] Research features are discoverable and maturity-tagged

## Phase 6: Alerts, Jobs, and Persistence

Goal:
Support durable workflows for alerts, saved charts, presets, and background jobs.

- [x] Add persistence model for jobs
- [x] Add persistence model for saved charts
- [x] Add persistence model for user presets
- [x] Separate alert rule management from alert scanning
- [x] Create `app/services/alerts/alert_rule_service.py`
- [x] Create `app/services/alerts/alert_scan_service.py`
- [x] Create `app/services/alerts/notification_service.py`
- [x] Add execution history for background scans
- [x] Add execution history for alerts
- [x] Add audit trails for workflow jobs
- [x] Design notification adapter boundaries for webhook/email/app delivery

Exit criteria:

- [x] Workflow entities persist cleanly
- [x] Alerts and jobs scale independently
- [x] Operational history is inspectable

## Phase 7: Public Surface Consolidation

Goal:
Make AstroSDK usable as a broader platform across API and SDK consumers.

- [x] Create `api/v2/astronomy`
- [x] Create `api/v2/western`
- [x] Create `api/v2/vedic`
- [x] Create `api/v2/mundane` (via common router)
- [x] Create `api/v2/research`
- [x] Create `api/v2/alerts`
- [x] Create `app/sdk/client.py`
- [x] Create grouped SDK modules for Western, Vedic, and research usage
- [x] Document capability registry usage
- [x] Document maturity levels and compatibility policy
- [x] Add examples for research/notebook usage

Exit criteria:

- [x] `api/v2` is aligned to architecture domains
- [x] Python SDK surface exists
- [x] Public compatibility expectations are documented

## Cross-Phase Quality Gates

These should remain active throughout the AstroSDK 2.0 rollout.

- [x] No new feature lands only in the old flat service layout
- [x] No new core calculation depends on hidden mode defaults
- [x] Experimental features are clearly marked
- [x] API responses include reproducibility metadata where applicable
- [x] Golden validation fixtures grow with feature coverage
- [x] Heavy scans move to worker-backed execution when needed
- [x] GitHub backlog stays aligned with implementation progress
