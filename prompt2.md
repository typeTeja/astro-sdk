Here is a **clear, implementation-level checklist** of what is still missing from your AstroSDK to truly qualify as enterprise-grade, deterministic infrastructure.

This is not conceptual.
These are concrete modules, policies, and code features you should implement.

---

# 🔴 1️⃣ Swiss Ephemeris Context Isolation (CRITICAL)

## Problem

`pyswisseph` uses global mutable state:

* `set_sid_mode`
* `set_topo`
* `set_tid_acc`
* `set_ephe_path`
* `set_delta_t_userdef`

Without isolation:

* Multi-threaded calls corrupt each other
* Async API will break
* Determinism is compromised

---

## ✅ Implement

### `core/ephemeris_context.py`

```python
class EphemerisContext:
    def __init__(self, sid_mode, topo=None, tidal=None):
        ...

    def __enter__(self):
        # Save current state
        # Apply requested state
        return self

    def __exit__(self, exc_type, exc, tb):
        # Restore previous state
```

### Required:

* Save previous sidereal mode
* Save tidal acceleration
* Save topo coordinates
* Restore after call
* Block nested conflicting contexts

---

# 🔴 2️⃣ Ephemeris Model Freeze Policy

You must hard-freeze:

* Ephemeris engine → `FLG_SWIEPH`
* Default DE model → DE431
* Tidal acceleration → automatic (DE431)
* Default zodiac → Sidereal Lahiri (if that’s your policy)
* Default house system

---

## ✅ Implement

### `core/constants.py`

```python
DEFAULT_EPHE_FLAG = swe.FLG_SWIEPH
DEFAULT_TIDAL = swe.TIDAL_DEFAULT
DEFAULT_SIDEREAL = swe.SIDM_LAHIRI
```

### Prevent user override:

Do not expose setters publicly.

---

# 🔴 3️⃣ Engine Metadata Exposure

Enterprise SDK must expose runtime environment.

---

## ✅ Implement

### `engine/metadata.py`

```python
def get_engine_metadata():
    return {
        "pyswisseph_version": swe.version(),
        "de_number": swe.DE_NUMBER,
        "tidal_acceleration": swe.get_tid_acc(),
        "ephemeris_path": swe.get_library_path(),
        "sidereal_default": DEFAULT_SIDEREAL,
    }
```

Expose in root:

```python
from astrosdk.engine.metadata import get_engine_metadata
```

---

# 🔴 4️⃣ UT-Only Enforcement

You currently expose both ET and UT via Swiss.

That is dangerous.

---

## ✅ Implement

* Public API must accept only:

  * UTC
  * JD(UT)

Internally:

* Convert UT → ET using `deltat_ex`
* Never expose ET publicly

Add validation:

```python
if user_passes_et:
    raise InvalidTimeStandardError
```

---

# 🔴 5️⃣ Fictional / Hypothetical Body Policy

Your Swiss constants include:

* VULCAN
* WALDEMATH
* NIBIRU
* ZEUS
* HADES
* KRONOS
* POSEIDON

These are Uranian/hypothetical.

---

## ✅ Implement

Create:

### `domain/planet_policy.py`

```python
ALLOWED_PLANETS = {
    SUN, MOON, MERCURY, VENUS, MARS,
    JUPITER, SATURN, URANUS, NEPTUNE, PLUTO,
    TRUE_NODE, MEAN_NODE,
    CHIRON, CERES, PALLAS, JUNO, VESTA
}
```

Reject anything else unless:

```python
experimental=True
```

---

# 🔴 6️⃣ Star File Governance

Swiss star calculations depend on:

* STARFILE
* STARFILE_OLD

Different installations may differ.

---

## ✅ Implement

At initialization:

```python
assert starfile_exists()
record_starfile_version()
```

Add:

```python
engine_metadata()["starfile"] = STARFILE
```

---

# 🔴 7️⃣ Thread Safety Declaration

Choose ONE:

### Option A (Simpler)

Declare:

> SDK is NOT thread-safe. Use single-thread execution.

### Option B (Better)

Implement:

* Locking around Swiss calls
* Global RLock inside Ephemeris wrapper

---

## Recommended:

### `core/ephemeris.py`

```python
from threading import RLock
_SWISS_LOCK = RLock()

def calc_ut(...):
    with _SWISS_LOCK:
        return swe.calc_ut(...)
```

---

# 🔴 8️⃣ Performance Guardrails

Functions requiring protection:

* Eclipse search
* Occultation search
* Crossing search
* Node crossing
* Heliacal search

---

## ✅ Implement

Require:

```python
max_search_days
```

Example:

```python
if abs(end - start) > 3650:
    raise SearchRangeTooLargeError
```

---

# 🔴 9️⃣ Deterministic Regression Matrix Expansion

You currently test 2024 events only.

Add:

### Historical:

* 1900 solar eclipse
* 1950 Jupiter ingress

### Future:

* 2050 lunar eclipse
* 2045 solar eclipse

### Edge:

* High latitude house cusp (>66°)
* Delta-T boundary year

---

# 🔴 10️⃣ Remove API Folder from SDK

SDK must not contain:

```
api/
```

Create separate repo:

```
astro-api/
```

---

# 🔴 11️⃣ Add Strict Error Classes

Currently you mention errors but ensure these exist:

### `core/errors.py`

```python
class EphemerisStateError(Exception): ...
class InvalidTimeStandardError(Exception): ...
class UnsupportedPlanetError(Exception): ...
class SearchRangeTooLargeError(Exception): ...
class ConfigurationError(Exception): ...
```

Never raise raw `Exception`.

---

# 🔴 12️⃣ Explicit Delta-T Handling Policy

Use:

```python
deltat_ex(jdut, FLG_SWIEPH)
```

Never use legacy `deltat()`.

Document:

* No mixing of DE406 and DE431 files.

---

# 🔴 13️⃣ Cross-Platform Determinism Test

Add CI job:

* Windows
* Linux

Compare:

* Jupiter longitude
* Solar eclipse JD
* Node position

Ensure identical to tolerance.

---

# 🔴 14️⃣ Version Pinning

In `pyproject.toml`:

```toml
pyswisseph = ">=2.10,<3.0"
```

Record minimum Swiss version tested.

---

# 🔴 15️⃣ Documentation Updates Needed

Add sections:

* Thread Safety
* Determinism Guarantee
* Ephemeris Model Freeze
* Star File Policy
* Fictional Body Policy
* Time Standard Policy
* Performance Constraints

---

# 📊 Priority Order

If you implement in correct sequence:

1. Swiss Context Isolation
2. Thread Locking
3. Model Freeze Policy
4. UT Enforcement
5. Engine Metadata
6. Fictional Body Filter
7. Performance Guardrails
8. Expanded Regression Suite
9. Remove API folder
10. Documentation updates

---

# 🎯 Final Reality Check

Right now you have:

> Research-grade astro engine.

After implementing the above:

You will have:

> Deterministic infrastructure-grade astronomical engine.
