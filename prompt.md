# ROLE

You are a:

* Senior Astronomy Systems Engineer
* Swiss Ephemeris Specialist
* Deterministic Engine Architect

Your mission is to:

1. Inspect the entire `pyswisseph` Python API surface.
2. Enumerate ALL supported astronomical calculations.
3. Categorize them into:

   * Core astrology
   * Advanced astronomy
   * Events
   * Eclipses
   * Houses
   * Nodes
   * Fixed stars
   * Phenomena
   * Misc astronomical utilities
4. Design a structured integration plan into `astrosdk`.
5. Implement supported calculations in a clean, layered architecture.
6. Maintain strict compliance with SDK architectural rules.

---

# HARD CONSTRAINTS

You MUST:

* Use Swiss Ephemeris only (no fallback engines)
* Maintain determinism
* Avoid interpretation logic
* Avoid prediction logic
* Avoid financial inference
* Avoid UI logic
* Avoid HTTP
* Avoid database
* Avoid ML
* Avoid LLM

All outputs must be:

* Typed
* Immutable
* Deterministic
* Explicitly configurable

---

# PHASE 1 — DISCOVERY (MANDATORY FIRST STEP)

Programmatically inspect:

```python
import swisseph as swe
dir(swe)
help(swe)
```

Extract and categorize:

* All functions beginning with:

  * `swe_`
  * `calc`
  * `fixstar`
  * `house`
  * `rise_trans`
  * `pheno`
  * `eclipse`
  * `heliacal`
  * `azalt`
  * `sidtime`
  * `julday`
  * `revjul`
  * `deltat`
  * `get_`
  * `set_`

Produce a structured list like:

```
Category: Planetary Positions
- swe.calc
- swe.calc_ut
- swe.set_sid_mode
- swe.set_topo
...
```

DO NOT implement anything yet.

Only produce:

* Full categorized capability report.

---

# PHASE 2 — ARCHITECTURAL MAPPING

For each function category:

Map it to one of:

```
core/
domain/
services/
engine/
events/
cycles/
```

Example:

| Swiss Function  | SDK Module             |
| --------------- | ---------------------- |
| swe.calc_ut     | core.ephemeris         |
| swe.houses_ex   | core.ephemeris         |
| swe.eclipse_lun | services.event_service |
| swe.pheno_ut    | services.planetary     |
| swe.fixstar_ut  | services.fixed_star    |
| swe.rise_trans  | services.event_service |

Reject any function that:

* Breaks determinism
* Introduces randomness
* Requires external unknown data
* Violates architecture guardrails

---

# PHASE 3 — SAFE EXPANSION CATEGORIES

You must implement only safe astronomical categories:

---

## 1️⃣ Planetary Calculations

* Longitude
* Latitude
* Speed
* Acceleration
* Distance
* Retrograde detection
* Helio vs Geo
* True vs Mean Node

---

## 2️⃣ Houses

* Whole Sign
* Placidus
* Koch
* Equal
* KP (if supported)

---

## 3️⃣ Fixed Stars

Wrap:

```
swe.fixstar_ut
```

Return:

* Longitude
* Latitude
* Magnitude
* Distance (if available)

---

## 4️⃣ Eclipses

Wrap:

* Solar eclipse
* Lunar eclipse
* Saros series
* Magnitude
* Next/previous eclipse search

Return structured `EclipseEvent`.

---

## 5️⃣ Phenomena

Wrap:

```
swe.pheno_ut
```

Return:

* Phase angle
* Illumination fraction
* Apparent magnitude
* Elongation

---

## 6️⃣ Rise/Set/Transit

Wrap:

```
swe.rise_trans
```

Return:

* Rise time
* Set time
* Upper transit
* Lower transit

Must require:

* Latitude
* Longitude
* Elevation

---

## 7️⃣ Sidereal Time

Wrap:

```
swe.sidtime
```

Return explicit float.

---

## 8️⃣ Delta-T

Wrap:

```
swe.deltat
```

Centralize in `core/time.py`.

---

## 9️⃣ Heliacal Phenomena (Optional Advanced)

Wrap only if deterministic and stable.

---

# DO NOT IMPLEMENT

* Any interpretation logic
* Any probabilistic scoring
* Any price-based correlation
* Any financial signal generation
* Any astro-intensity scoring yet
* Any UI helper formatting

---

# ARCHITECTURE ENFORCEMENT

All new Swiss wrappers must:

* Live inside `core/ephemeris.py`
* Never leak raw Swiss arrays
* Convert to typed dataclasses
* Raise structured SDK exceptions
* Be fully documented

Example:

```python
@dataclass(frozen=True)
class PlanetPosition:
    longitude: float
    latitude: float
    speed: float
    retrograde: bool
```

Never return tuple outputs from swe directly.

---

# TESTING REQUIREMENTS

For every wrapped function:

* Add unit test
* Add edge case test
* Add regression comparison (known date)

Tolerance must be defined explicitly.

No silent tolerance widening.

---

# FINAL DELIVERABLE

Produce:

1. Swiss Ephemeris capability report
2. Categorized integration map
3. Implementation plan
4. Full updated SDK structure
5. Wrapped implementations
6. Tests for each new capability
7. Documentation update listing supported Swiss features

---

# CRITICAL WARNING

Do NOT blindly wrap entire Swiss Ephemeris surface.

This SDK must remain:

* Focused
* Deterministic
* Maintainable
* Auditable
* Financially safe

Accuracy > Feature count.

If a feature increases complexity without strategic value — exclude it and document why.

