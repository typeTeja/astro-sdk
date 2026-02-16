# 🚀 ASTRO SDK – FULL STRUCTURAL REFACTOR PROMPT

You are a **Senior Software Architect and Astro-Systems Engineer**.

You are performing a **full structural refactor of the Astro SDK**.

Important constraints:

* The SDK is NOT in production.
* Backward compatibility is NOT required.
* You may introduce breaking changes.
* You may refactor, rename, move, or delete any module.
* You may redesign the public interface.
* Architecture correctness > feature preservation.

Your goal is to:

> Convert the SDK into a fully typed, deterministic, domain-pure calculation engine with strict architectural boundaries.

---

# 🎯 Phase 8 – Domain & Architectural Alignment

## 1️⃣ Eliminate All Raw Dict Passing

* Replace all dict-based inputs/outputs with Pydantic v2 models.
* No dictionaries may cross module boundaries.
* All services must return typed models.
* Public SDK interface must return structured models.

---

## 2️⃣ Enforce Layer Separation

Ensure strict separation:

* `core/` → Swiss Ephemeris & time utilities only.
* `domain/` → Pure astrology math (no I/O).
* `services/` → Orchestration only.
* No astrology logic in service orchestration.
* No Swiss calls inside domain logic.
* No circular dependencies.

You may move or rename files to achieve clarity.

---

## 3️⃣ Stabilize Time & Determinism

* Centralize all time handling into a single module.
* Enforce explicit date, time, timezone.
* Remove any `now()` usage.
* Ensure Julian Day conversion is deterministic and reproducible.
* Validate timezone inputs strictly.

---

## 4️⃣ Redesign Public SDK Interface

Create a clean public interface such as:

```python
from astrosdk import calculate_natal_chart
from astrosdk import calculate_transits
```

Ensure:

* Minimal public surface area.
* Clear typed input models.
* Clear typed output models.
* No leaking internal structures.

You may redesign the entire API.

---

## 5️⃣ Freeze Domain Models

Define canonical models:

* PlanetPosition
* ChartAngles
* HouseCusp
* Aspect
* Transit
* Chart
* Panchanga (future-ready)

Models must be:

* Immutable where possible
* Fully typed
* Explicit in zodiac & ayanamsa
* Deterministic

---

# 🔥 Phase 9 – Higher-Order Domain Enhancements

After structural stabilization:

Implement missing domain logic cleanly:

## Combustion Logic

* Orb-based combustion rules.
* Configurable thresholds.
* Structured result (boolean + orb distance).

## Essential Dignities

* Exaltation
* Debilitation
* Own sign
* Moolatrikona
* Enemy/friend structure
* Enum-based classification

Must be:

* Pure domain math
* Configurable
* Test-covered

---

# 🧪 Testing Requirements

* Add regression tests for:

  * Julian Day conversion
  * Ascendant calculation
  * Aspect detection
  * Combustion detection
  * Dignity classification

* Remove brittle tests tied to dict structures.

* Ensure deterministic outputs.

---

# 🧹 Refactor Freedom

You are allowed to:

* Delete unused modules
* Rename files for clarity
* Move logic between layers
* Simplify abstractions
* Remove dead code
* Break old interfaces

But you must:

* Keep Swiss Ephemeris as the only astronomical source.
* Keep calculations deterministic.
* Keep domain pure.
* Maintain clean layering.

---

# 📊 Required Output From Refactor

After completion, provide:

1. New folder structure.
2. List of breaking changes introduced.
3. Public SDK interface documentation.
4. List of removed modules.
5. Summary of architectural improvements.
6. Technical debt removed.
7. Areas still needing improvement.

---

# 🎯 Success Criteria

The SDK should become:

* Fully typed
* Deterministic
* Purely domain-driven
* Infrastructure-ready
* Extensible without refactoring core
* Clean enough to wrap with FastAPI later without internal changes
