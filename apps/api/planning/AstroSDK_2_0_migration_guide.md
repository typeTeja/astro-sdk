# AstroSDK 2.0 Migration Guide

This document defines how AstroSDK should migrate from the current mixed
architecture into the AstroSDK 2.0 structure.

## Purpose

AstroSDK 2.0 is a guided migration, not a rewrite-first effort.

The goal is to:

- preserve current runtime behavior
- stop architecture drift
- make all new work land in the 2.0 shape by default
- migrate old modules gradually and safely

## Golden Rule

New AstroSDK 2.0 work should be added to the grouped 2.0 layout first.

Do not add brand-new feature logic to the old flat structure unless:

- the change is a small bug fix in an existing file
- the change is required to stabilize current production behavior
- migrating that path immediately would create unnecessary risk

## Placement Rules

### Put code in `app/core` when it is:

- Swiss Ephemeris runtime handling
- locking and global state safety
- time conversion primitives
- shared constants and enums
- deterministic metadata and fingerprinting
- capability registration

### Put code in `app/contexts` when it describes:

- calculation mode
- zodiac mode
- coordinate system
- observer location
- house system
- feature maturity or execution behavior
- search tolerances or precision

### Put code in `app/domain/*` when it is:

- an immutable engine output
- a value object
- a typed event/result structure
- a calculation model that should outlive any one API route

Domain code must not depend on API schemas.

### Put code in `app/services/*` when it is:

- feature logic
- orchestration within one astrology domain
- a calculation workflow that consumes contexts and returns domain objects

Services should not define HTTP behavior.

### Put code in `app/api/*` when it is:

- route definitions
- request parsing
- schema mapping
- response adaptation
- dependency wiring

Routers should not own business logic.

### Put code in `app/sdk` when it is:

- a public Python consumption surface
- a typed client or facade over engine services
- notebook and research-facing wrappers

### Put code in `app/workers` when it is:

- background execution
- long-running scan work
- dataset export jobs
- alert execution workflows

## Migration Strategy

Use this order whenever possible:

1. Add a 2.0 domain object.
2. Add or update a context object if needed.
3. Add a grouped 2.0 service.
4. Adapt old API routes to call the new service.
5. Remove or shrink old service logic only after parity is verified.

This avoids breaking current endpoints while still moving the center of gravity
toward the new architecture.

## Allowed Transitional Patterns

These are acceptable during migration:

- old routes calling new grouped services
- compatibility adapters that translate old arguments into `CalculationContext`
- domain models coexisting with legacy schema-style mapping
- `api/v1` reusing 2.0 services internally

## Discouraged Patterns

Avoid these unless there is a strong short-term reason:

- adding major new logic to old flat services
- introducing new raw booleans for sidereal/heliocentric mode when a context is available
- returning new dictionary payloads when a domain object should exist
- making `api/v1` the source of truth for new feature contracts

## Context Rules

All new calculation-oriented services should prefer `CalculationContext`.

If a new service cannot use the full top-level context yet, it may accept a more
focused context such as:

- `ZodiacContext`
- `CoordinateContext`
- `ObserverContext`
- `FeatureContext`

But new work should move toward the full context model over time.

## Feature Maturity Rules

Every significant new capability should declare a maturity level:

- `experimental`
- `beta`
- `production`

Use these rules:

- experimental: incomplete or still changing significantly
- beta: functionally usable but not yet final
- production: stable, deterministic, and supported

Do not expose unfinished features as if they were production-ready.

## API Rules During Migration

### `/api/v1`

Use for:

- preserving compatibility
- incremental cleanup
- adapting current routes to 2.0 internals

### `/api/v2`

Use for:

- grouped route families
- explicit context-driven contracts
- improved metadata
- cleaner long-term public design

## Testing Rules

Every migration step should add or preserve:

- unit coverage for new contexts/domain objects
- regression coverage for behavior parity
- focused tests for mode handling
- reproducibility metadata checks where applicable

## Definition Of Done For A Successful Migration Step

A migration step is complete when:

- the new code lives in the 2.0 structure
- behavior is covered by tests
- the old route or caller can use the new code safely
- no architecture drift was introduced

## Immediate Working Rule

From this point forward:

- new foundational code should land in the 2.0 layout
- current production fixes may still touch legacy files
- migration work should prefer adding adapters over risky rewrites
