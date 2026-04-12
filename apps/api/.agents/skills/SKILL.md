---
name: astrosdk-engineering
description: >
  Production-grade engineering and domain-knowledge skills for the AstroSDK 2.0 project.
  Covers Namespaced Services, CalculationContext, API v2, Swiss Ephemeris handling, 
  FastAPI architecture, and quality standards for the graduated 2.0 platform.
---

# AstroSDK 2.0 Engineering & Domain Skills

## §0 — Project Philosophy (Non-Negotiable)

AstroSDK is **infrastructure, not an application**. Every decision must be
evaluated against these axioms in strict priority order:

1. **Correctness > Performance > Convenience**
2. **Determinism is a contract** — same input → identical output, forever.
3. **Explicitness over brevity** — all parameters must be visible at the call site.
4. **Auditability (CalculationContext)** — every result must carry the full calculation context fingerprint in its `meta` block.
5. **No interpretation logic** — the SDK emits raw astronomical facts; callers assign meaning.

Violating any of these is a breaking change regardless of version impact.

---

## §1 — Repository Structure (Pure 2.0)

The repository follows a strict namespaced domain-driven design:

```
app/
├── core/           # LOW-LEVEL: Swiss Ephemeris singleton, thread lock, time, constants, errors
├── domain/         # MODELS: Subdivided by domain (astronomy, western, vedic, mundane, research, common)
├── services/       # LOGIC: Subdivided by domain. All services MUST accept a CalculationContext.
├── api/v2/         # HTTP LAYER: FastAPI routers for the 2.0 platform. Thin, validation + delegation.
├── schemas/        # PYDANTIC: request/response contracts subdivided by domain.
├── contexts/       # ARCHITECTURE: CalculationContext definitions and factory patterns.
└── models/         # ORM: SQLModel persistence models — alerts only.
```

**Dependency Direction (Pure 2.0):**
```
api/v2 → contexts → services → domain ← core
          api/v2 → schemas → domain
```

---

## §2 — Calculation Context Pattern

Every calculation requires a `CalculationContext`. This context encapsulates:
- **Zodiac**: Sidereal/Tropical mode, Ayanamsa selection, Heliocentric/Geocentric.
- **Location**: Latitude, Longitude, Altitude.
- **Features**: List of active high-level capabilities.
- **Audit**: Metadata tracking for the calculation fingerprint.

**Usage:**
```python
from app.contexts.factories import create_default_context
context = create_default_context()
service = WesternChartService(context, ephemeris=ephemeris)
```

---

## §3 — Swiss Ephemeris Handling Rules

### §3.1 — The Global Lock
`pyswisseph` is a C-extension wrapping a **global mutable C library**. All calls
must go through `_SWISS_LOCK = RLock()` defined in `app/core/ephemeris.py`.

**Rules:**
- Every `swe.*` call MUST be inside `with _SWISS_LOCK:`.
- Never call `swe.*` directly from services or routers — always go through `Ephemeris`.
- `Ephemeris` is a singleton. Access via `get_ephemeris` dependency injection.

### §3.2 — Temporal Precision
All internal time-series calculations MUST use Julian Day (JD) as the atomic
temporal unit. 
- **Time normalisation**: `app/core/time.py` correctly handles UTC normalization and JD conversion using the `86400.0` divisor.
- **Delta-T**: Always applied at the core level to ensure Dynamical Time (ET) precision.

### §3.3 — Sidereal Mode Handling
The `CalculationContext` manages sidereal state. The `Ephemeris` singleton internally handles the `set_sid_mode()` calls within the global lock to prevent race conditions during concurrent requests.

---

## §4 — Domain Modeling & Schemas

### §4.1 — Immutable Domain Models
All domain objects in `app/domain/` are `@dataclass(frozen=True)`. Changes require creating new instances.

### §4.2 — Namespace Alignment
Domain models, Services, and Schemas must follow the same namespacing:
- `astronomy`: Basic planetary math, cycles, and horizon events.
- `western`: Charts, aspects, progressions, synastry.
- `vedic`: Panchanga, Dashas, Varga math, Shadbala.
- `mundane`: Global events, ingresses, stations.
- `research`: Quantitative analysis, financial correlations.

### §4.3 — Response Envelope
Every endpoint returns a `BaseAstroResponse` which mirrors the `CalculationContext` in its `meta` block, ensuring identical results are reproducible by any client.

---

## §5 — API Design (v2)

### §5.1 — No Business Logic in Routers
Routers are thin wrappers. They validate input via Pydantic and delegate to a namespaced Service.

### §5.2 — Dependency Injection
Always use FastAPI `Depends()` for `Ephemeris` and `Service` instantiation. This ensures the singleton pattern is respected and enables clean testing.

### §5.3 — Error Handling
Centralized exception handlers in `app/main.py` map `AstroError` subclasses to correct HTTP status codes (400 for input errors, 500 for calculation failures).

---

## §6 — Performance & Testing

### §6.1 — Concurrency
While Swiss Ephemeris is serialized via a lock, I/O bound tasks (Database, Background Tasks) must be asynchronous to ensure high throughput for the FastAPI workers.

### §6.2 — Testing Standards (mypy strict)
- ALL code must pass `mypy --strict`.
- Every astronomical service MUST have at least one regression test against "Golden Values" (known good data).
- Regression tests MUST NOT mock the ephemeris.

---

## §7 — Anti-Patterns (NEVER DO THESE)
1. **Direct `swisseph` calls**: Any call outside `app/core/ephemeris.py` is a violation.
2. **Business Logic in Routers**: Routers calculate nothing.
3. **Naïve Datetimes**: All times must be UTC-aware.
4. **Missing Type Annotations**: Every function must be fully annotated.
5. **Interpretation**: Never output "Good/Bad" or "Lucky" — output only degrees, angles, and names.

---
*This file is the single source of truth for all engineering and domain decisions in the AstroSDK 2.0 project.*
