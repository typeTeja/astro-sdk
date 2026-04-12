# AstroSDK 2.0 Architecture Roadmap

## Purpose

AstroSDK 2.0 should evolve from a broad FastAPI astrology backend into a long-lived
calculation platform: deterministic at the core, modular across traditions, and
stable enough to support desktop, mobile, and web products from the same engine.

This roadmap turns that goal into:

- a target architecture
- a concrete folder structure
- an implementation sequence
- a milestone backlog

## Vision

AstroSDK 2.0 should be:

- a deterministic astronomy and astrology engine
- a backend-first platform that can serve web, mobile, and desktop apps
- a multi-tradition system that supports Western, Vedic, research, and mundane workflows
- a feature platform where every result is reproducible and every capability has a maturity level

## Core Principles

1. Correctness over feature count.
2. Determinism is a product contract.
3. Calculation context must always be explicit.
4. Swiss Ephemeris global state must be isolated behind one safety boundary.
5. Domain models must be richer than the API layer.
6. Experimental features must be visibly marked and structurally separated.
7. Astronomy facts, astrology derivations, and interpretations must stay separate.

## Target Architecture

AstroSDK 2.0 should be organized into five layers:

### 1. Core Runtime

Responsible for:

- Swiss Ephemeris access
- time normalization
- locks and global state management
- constants, enums, and errors
- engine versioning and calculation fingerprinting

This layer should know nothing about HTTP or product presentation.

### 2. Context Layer

All calculations should run with explicit context objects instead of loose flags.

Recommended context objects:

- `CalculationContext`
- `TimeContext`
- `ObserverContext`
- `ZodiacContext`
- `CoordinateContext`
- `HouseContext`
- `FeatureContext`

These objects should fully describe:

- tropical vs sidereal
- ayanamsa
- geocentric vs heliocentric vs topocentric
- observer coordinates
- house system
- precision and search tolerances
- feature maturity level

### 3. Domain Layer

This is the long-term heart of AstroSDK.

It should contain immutable value objects for:

- planet positions
- chart structures
- aspects
- transit windows
- returns
- progressions
- dasha periods
- nakshatra and pada positions
- varga charts
- yogas
- fixed star contacts
- declination aspects
- mundane ingresses
- research series

The API should never be the source of truth for engine design. The domain layer should be.

### 4. Feature Services

Services should be grouped by domain, not by route growth.

Recommended service families:

- astronomy
- western
- vedic
- mundane
- research
- alerts

Each family should expose pure calculation services that accept context objects and
return domain objects.

### 5. Delivery Layer

The delivery layer should adapt the engine for different surfaces:

- HTTP API
- Python SDK
- background workers
- future CLI or local app adapters

This layer should map domain objects outward, never define engine rules inward.

## Feature Maturity Model

Every capability should carry one maturity level:

- `experimental`
- `beta`
- `production`

Rules:

- experimental features may change without compatibility guarantees
- beta features should be correct but still evolving
- production features must preserve determinism and API stability

The maturity level should appear in:

- internal capability registry
- API metadata
- docs
- tests

## Concrete Folder Structure

Below is the recommended AstroSDK 2.0 folder layout.

```text
app/
├── api/
│   ├── common/
│   │   ├── dependencies.py
│   │   ├── errors.py
│   │   └── metadata.py
│   ├── v1/
│   │   ├── astronomy/
│   │   ├── western/
│   │   ├── vedic/
│   │   ├── research/
│   │   ├── mundane/
│   │   └── alerts/
│   └── v2/
│       ├── astronomy/
│       ├── western/
│       ├── vedic/
│       ├── research/
│       ├── mundane/
│       └── alerts/
├── contexts/
│   ├── calculation.py
│   ├── coordinate.py
│   ├── feature.py
│   ├── house.py
│   ├── observer.py
│   ├── time.py
│   └── zodiac.py
├── core/
│   ├── constants.py
│   ├── ephemeris.py
│   ├── ephemeris_context.py
│   ├── errors.py
│   ├── fingerprint.py
│   ├── locks.py
│   ├── metadata.py
│   ├── precision.py
│   ├── registry.py
│   └── time.py
├── domain/
│   ├── astronomy/
│   │   ├── eclipse.py
│   │   ├── fixed_star.py
│   │   ├── horizon.py
│   │   ├── house.py
│   │   ├── lunar.py
│   │   └── planet.py
│   ├── common/
│   │   ├── enums.py
│   │   ├── identifiers.py
│   │   └── metadata.py
│   ├── mundane/
│   │   ├── ingress.py
│   │   ├── mundane_event.py
│   │   └── station.py
│   ├── research/
│   │   ├── correlation.py
│   │   ├── dataset.py
│   │   └── series.py
│   ├── vedic/
│   │   ├── ashtakavarga.py
│   │   ├── dasha.py
│   │   ├── nakshatra.py
│   │   ├── shadbala.py
│   │   ├── varga.py
│   │   └── yoga.py
│   └── western/
│       ├── aspect.py
│       ├── chart.py
│       ├── composite.py
│       ├── progression.py
│       ├── return_chart.py
│       ├── synastry.py
│       └── transit.py
├── engine/
│   ├── astronomy_engine.py
│   ├── mundane_engine.py
│   ├── research_engine.py
│   ├── vedic_engine.py
│   └── western_engine.py
├── models/
│   ├── alerts.py
│   ├── jobs.py
│   ├── presets.py
│   └── saved_charts.py
├── schemas/
│   ├── common/
│   ├── astronomy/
│   ├── western/
│   ├── vedic/
│   ├── research/
│   ├── mundane/
│   └── alerts/
├── services/
│   ├── alerts/
│   │   ├── alert_rule_service.py
│   │   ├── alert_scan_service.py
│   │   └── notification_service.py
│   ├── astronomy/
│   │   ├── eclipse_service.py
│   │   ├── fixed_star_service.py
│   │   ├── horizon_service.py
│   │   ├── house_service.py
│   │   ├── lunar_service.py
│   │   └── planetary_service.py
│   ├── mundane/
│   │   ├── event_service.py
│   │   ├── ingress_service.py
│   │   └── station_service.py
│   ├── research/
│   │   ├── export_service.py
│   │   ├── scan_service.py
│   │   └── statistics_service.py
│   ├── vedic/
│   │   ├── ashtakavarga_service.py
│   │   ├── dasha_service.py
│   │   ├── nakshatra_service.py
│   │   ├── shadbala_service.py
│   │   ├── varga_service.py
│   │   └── yoga_service.py
│   └── western/
│       ├── aspect_service.py
│       ├── chart_service.py
│       ├── composite_service.py
│       ├── progression_service.py
│       ├── return_service.py
│       ├── synastry_service.py
│       └── transit_service.py
├── sdk/
│   ├── client.py
│   ├── contexts.py
│   ├── western.py
│   ├── vedic.py
│   └── research.py
├── workers/
│   ├── alert_worker.py
│   ├── export_worker.py
│   └── scan_worker.py
└── main.py

tests/
├── contract/
├── fixtures/
├── golden/
├── integration/
├── performance/
├── regression/
├── unit/
│   ├── contexts/
│   ├── core/
│   ├── domain/
│   ├── services/
│   └── engines/
└── validation/
```

## Migration Strategy From Current Structure

The current repository already has a useful foundation, so AstroSDK 2.0 does not
need a rewrite-first strategy.

Recommended migration approach:

1. Keep the current app running.
2. Introduce new `contexts/`, `domain/*`, and grouped `services/*` modules in parallel.
3. Move new work into the 2.0 structure first.
4. Gradually adapt old routers to the new services.
5. Build `api/v2` only after the core service contracts stabilize.

This avoids breaking momentum while improving architecture.

## Domain Expansion Priorities

To support real-world astrology at depth, these domain objects should be added early:

### Western

- `TransitWindow`
- `ReturnChart`
- `ProgressedChart`
- `DirectedEvent`
- `SynastryAspect`
- `CompositeChart`
- `DeclinationAspect`
- `ParanEvent`

### Vedic

- `NakshatraPosition`
- `PadaPosition`
- `DashaPeriod`
- `VargaChart`
- `YogaHit`
- `AshtakavargaMatrix`
- `ShadbalaScore`

### Research And Mundane

- `ResearchSeries`
- `MarketCycleCorrelation`
- `MundaneIngress`
- `EventCluster`
- `SignalScore`

## API Strategy

AstroSDK should treat the API as a delivery contract, not the engine itself.

### Keep `/api/v1`

Use `/api/v1` for:

- stable legacy routes
- gradual cleanup
- compatibility for existing clients

### Introduce `/api/v2`

Use `/api/v2` for:

- grouped route families
- explicit context objects
- cleaner metadata contracts
- capability and maturity reporting

### Recommended Route Families In v2

- `/api/v2/astronomy`
- `/api/v2/western`
- `/api/v2/vedic`
- `/api/v2/mundane`
- `/api/v2/research`
- `/api/v2/alerts`

## Persistence Strategy

AstroSDK should remain calculation-stateless where possible, but persist workflow entities.

Persist:

- saved charts
- user presets
- alert rules
- async jobs
- exported datasets
- audit logs for long-running tasks

Do not persist:

- derived calculation state that should be recomputed deterministically

## Scalability Strategy

AstroSDK can scale well as a backend platform, but Swiss Ephemeris imposes runtime constraints.

Recommended model:

- stateless API workers
- separate long-running research workers
- separate alert scanning workers
- horizontal scaling by process and instance
- deterministic result caching for repeat requests

Avoid:

- over-reliance on thread-level concurrency within one process
- mixing request/response APIs with long-running research jobs in the same execution path

## Test Architecture

For a long-lived astrology platform, testing must become part of the architecture.

Required test layers:

- unit tests for domain math
- regression tests for known events
- contract tests for API schemas
- integration tests for full route behavior
- golden dataset validation
- performance tests for long scans

Golden fixtures should include:

- eclipse dates
- ingress dates
- retrograde stations
- known natal charts
- nakshatra and dasha examples
- varga outputs
- fixed star contacts
- paran and declination examples

## Milestone Backlog

The backlog below is intentionally concrete and sequenced.

### Milestone 0: Architecture Baseline

Goal:
Create the internal structure needed for 2.0 work without breaking current production flow.

Tasks:

- add `contexts/` package
- add grouped domain namespaces under `domain/`
- add grouped service namespaces under `services/`
- add `core/registry.py` for capability and maturity metadata
- define a `FeatureMaturity` enum
- define a `CalculationContext` base model
- document migration rules for old modules

Exit criteria:

- new architectural spine exists
- no breaking API changes
- all new features must use the 2.0 layout

### Milestone 1: Core Determinism Hardening

Goal:
Make mode handling and Swiss Ephemeris state management fully explicit and safe.

Tasks:

- unify all state mutation behind shared Swiss locks
- remove implicit mode switching
- replace loose flags with context objects in new services
- add calculation fingerprinting to metadata
- add explicit geo/helio/topo contract tests
- add explicit tropical/sidereal parity tests

Exit criteria:

- all core calculations use explicit context
- state safety rules are centralized
- deterministic metadata includes calculation fingerprint

### Milestone 2: Western Core 2.0

Goal:
Stabilize the most common Western features on the new architecture.

Tasks:

- build `western/chart_service.py`
- build `western/transit_service.py`
- build `western/aspect_service.py`
- add `ReturnChart` and `TransitWindow`
- implement return chart APIs in `v2`
- implement synastry and composite domain models
- define maturity levels for all Western endpoints

Exit criteria:

- natal, transits, aspects, and returns are first-class 2.0 services
- `api/v2/western` is usable

### Milestone 3: Vedic Core 2.0

Goal:
Promote Vedic support from partial feature collection into a structured subsystem.

Tasks:

- add `NakshatraPosition`, `PadaPosition`, `DashaPeriod`, `VargaChart`
- split current Vedic logic into dedicated services
- formalize varga calculation contracts
- add vimshottari dasha service
- add ashtakavarga and shadbala maturity levels
- add validation fixtures for classical Vedic examples

Exit criteria:

- Vedic feature family has domain-first architecture
- `/api/v2/vedic` exists with explicit maturity metadata

### Milestone 4: Mundane And Event Engine

Goal:
Support real-world event scanning with durable abstractions.

Tasks:

- introduce `MundaneIngress`, `StationEvent`, `EventCluster`
- split ingress, station, eclipse, and macro event logic into `services/mundane`
- build event scan jobs for large time windows
- add historical validation fixtures
- define event search tolerances in context models

Exit criteria:

- mundane/event calculations are no longer scattered across generic services
- large event scans can run as background jobs

### Milestone 5: Research Platform

Goal:
Turn the engine into a strong research backend.

Tasks:

- add `ResearchSeries`, `DatasetExport`, `MarketCycleCorrelation`
- build export worker and scan worker
- support CSV/JSON research datasets
- add job persistence and result retrieval
- add capability reporting for research features

Exit criteria:

- large scans and exports no longer depend on request-time execution
- research workflows are first-class

### Milestone 6: Alerts, Jobs, And Persistence

Goal:
Support product workflows beyond direct calculations.

Tasks:

- add job models
- add saved chart models
- add preset models
- separate alert rule and alert scan responsibilities
- add execution history for alert scans
- prepare notification adapters

Exit criteria:

- alerts and jobs are durable system features
- persistence layer matches long-term product needs

### Milestone 7: Public Surface Consolidation

Goal:
Make AstroSDK usable as a platform, not only a REST backend.

Tasks:

- publish a first-party Python SDK
- expose grouped engine clients
- document capability registry usage
- document maturity levels and compatibility policy
- expand examples for web/mobile/desktop backend usage

Exit criteria:

- AstroSDK can be consumed by backend clients and analyst workflows cleanly

## Suggested Execution Timeline

### Quarter 1

- Milestone 0
- Milestone 1

### Quarter 2

- Milestone 2
- Milestone 3

### Quarter 3

- Milestone 4
- Milestone 5

### Quarter 4

- Milestone 6
- Milestone 7

## Recommended Engineering Rules For 2.0

1. No new feature should enter the old flat service layout.
2. No new calculation should rely on hidden mode defaults.
3. Every new feature must declare its maturity level.
4. Every new API response must carry reproducibility metadata.
5. Experimental features must never masquerade as production-ready outputs.
6. Long-running scans must move to workers once they outgrow request-time execution.
7. Golden test fixtures should grow alongside feature coverage.

## Final Recommendation

AstroSDK 2.0 should not be a rewrite of everything at once. It should be a guided
migration toward a domain-first calculation platform.

The most important shift is this:

- stop organizing growth around endpoints
- start organizing growth around calculation domains and explicit contexts

If that shift happens early, AstroSDK can realistically support a very large
subset of real-world astrology features over a long project lifespan without
turning into an unmaintainable monolith.
