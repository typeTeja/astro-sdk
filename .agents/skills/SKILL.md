---
name: astrosdk-engineering
description: >
  Production-grade engineering and domain-knowledge skills for the AstroSDK project.
  Covers Swiss Ephemeris handling, FastAPI architecture, astrology correctness,
  scaling patterns, anti-patterns, and quality standards. Required reading for all
  AI agents working on this codebase.
---

# AstroSDK Engineering & Domain Skills

## §0 — Project Philosophy (Non-Negotiable)

AstroSDK is **infrastructure, not an application**. Every decision must be
evaluated against these axioms in strict priority order:

1. **Correctness > Performance > Convenience**
2. **Determinism is a contract** — same input → identical output, forever
3. **Explicitness over brevity** — all parameters must be visible at the call site
4. **Auditability** — every result must carry the full calculation context in its `meta` block
5. **No interpretation logic** — the SDK emits raw astronomical facts; callers assign meaning

Violating any of these is a breaking change regardless of version impact.

---

## §1 — Repository Structure

```
app/
├── core/           # LOW-LEVEL: Swiss Ephemeris singleton, thread lock, time, constants, errors
├── domain/         # PURE MODELS: frozen dataclasses only — no I/O, no business logic
├── services/       # BUSINESS LOGIC: pure-function classes receiving Ephemeris, returning domain objects
├── engine/         # FACADE: high-level orchestration (ChartEngine) — composes services
├── api/v1/         # HTTP LAYER: FastAPI routers — thin, validation + delegation only
├── schemas/        # PYDANTIC: request/response contracts — never domain logic
└── models/         # ORM: SQLModel persistence models — alerts only currently
```

**Dependency Direction (strict, no reversals allowed):**
```
api/v1 → schemas → services → domain ← core
                  services → core
         engine → services → core
```

Never import from `api/` inside `services/`, `domain/`, or `core/`.
Never import from `schemas/` inside `domain/` or `core/`.
Never import from `services/` inside `core/` or `domain/`.

---

## §2 — Swiss Ephemeris Handling Rules

### §2.1 — The Global Lock

`pyswisseph` is a C-extension wrapping a **global mutable C library**. All calls
must go through `_SWISS_LOCK = RLock()` defined in `app/core/ephemeris.py`.

**Rules:**
- Every `swe.*` call MUST be inside `with _SWISS_LOCK:`.
- Never call `swe.*` directly from services or routers — always go through `Ephemeris`.
- The `Ephemeris` class is a singleton (`__new__` pattern). Use it via dependency injection, not re-instantiation.

### §2.2 — Julian Day is the Canonical Time Unit

All internal time-series calculations MUST use Julian Day (JD) as the atomic
temporal unit. Never use Python `datetime` inside calculation loops.

- JD is a continuous real number with no time-zone, leap-second, or DST ambiguity.
- `Time.julian_day` is the only value passed to `Ephemeris` methods.
- `Time` objects are created from timezone-aware `datetime` and immediately normalized to UTC.
- **Bug in `core/time.py` (known):** `d = ... + dt.second / 84600.0` — the
  correct divisor is `86400.0` (seconds per day). The `84600` value introduces
  a ~2.8-second systematic error per second of offset. **Fix this before any
  high-precision temporal scan.**

### §2.3 — Sidereal Mode is Global State

`swe.set_sid_mode()` mutates the C library's global sidereal state. This means:

- Never call `set_sidereal_mode()` without holding `_SWISS_LOCK`.
- Use `EphemerisContext` for any temporary mode switch — it guarantees restoration.
- The project default is `SiderealMode.LAHIRI`. All services that accept
  `sidereal_mode` must pass it explicitly and never hardcode it.
- `EphemerisContext.__exit__` currently always restores to `LAHIRI` regardless
  of what the previous mode was. This is adequate for single-mode callers but
  **will break nested context usage**. Track the previous mode from `swe.get_ayanamsa_ut`
  or a module-level variable before overwriting.

### §2.4 — Planetary Body IDs

Use only `Planet` enum values (defined in `core/constants.py`). Never pass raw
integers to `Ephemeris` methods. Every method that accepts `planet: Planet`
must validate against `ALLOWED_PLANETS` before the lock.

Special bodies:
- `Planet.MEAN_NODE_OPP` (`-1`) is the synthetic Ketu node — not a real SE ID.
  It must be skipped in `iterate over Planet` loops (see `natal_service.py`).
- `Planet.LILITH_MEAN` (12) and `Planet.LILITH_TRUE` (13) are valid SE IDs.
- `Planet.CHIRON` (15), `Planet.CERES` (17-20) are valid asteroid IDs.

### §2.5 — Flags

Always compose flags explicitly:
```python
flags = DEFAULT_EPHE_FLAG | swe.FLG_SPEED            # mandatory for velocity
flags |= swe.FLG_SIDEREAL if sidereal else 0
flags |= swe.FLG_HELCTR   if heliocentric else 0
flags |= swe.FLG_TOPOCTR  if topocentric else 0
```

`DEFAULT_EPHE_FLAG = 2` (SE_FLG_SWIEPH) — always use the Swiss Ephemeris file
engine, never JPL unless explicitly requested and files are present.

### §2.6 — House Systems

`swe.houses()` returns tropical cusps. The sidereal correction (ayanamsa
subtraction) is applied manually in `Ephemeris.calculate_houses()`.

- Placidus and Koch fail at extreme latitudes (>65°N or <65°S). The fallback
  implemented in `NatalService.calculate_houses()` (falls back to Porphyry) is
  correct.
- Always validate house system before calling — use the `HouseSystem` enum.
- Whole-Sign and Equal house systems are independent of latitude and always safe.

### §2.7 — Eclipse Magnitude

`swe.sol_eclipse_when_glob()` returns a bitmask type code, not a float
magnitude. The current `search_solar_eclipse()` hardcodes `magnitude: 1.0`,
which is incorrect. The actual magnitude is in `res[1][2]` (the `tret` array at
index 2 for central eclipse). Fix: extract `tret[1]` for the magnitude.

---

## §3 — Domain Modeling Rules

### §3.1 — Domain Objects are Frozen

All domain objects MUST be `@dataclass(frozen=True)`. They are value objects —
no setters, no mutation, no in-place updates. If you need to modify a domain
object, create a new one.

### §3.2 — Domain vs Schema Separation

| Layer | Purpose | Example |
|---|---|---|
| `domain/` | Internal model used by services and engine | `PlanetPosition`, `Aspect` |
| `schemas/` | Pydantic models for HTTP request/response | `PlanetPositionData`, `NatalChartResponse` |

Services return domain objects. Routers convert domain → schemas. Never expose
domain dataclasses in API responses directly.

### §3.3 — AstroEvent Type System

`AstroEvent.type` is currently a plain `str`. This is a gap — it must be an
enum to enforce correctness. Define:

```python
class AstroEventType(StrEnum):
    INGRESS = "INGRESS"
    STATION = "STATION"
    ASPECT = "ASPECT"
    ECLIPSE = "ECLIPSE"
    SYNODIC = "SYNODIC"
    RETURN = "RETURN"
    PARAN = "PARAN"
    HELIACAL = "HELIACAL"
```

### §3.4 — ZodiacSign Mapping

`ZodiacSign(int(longitude / 30))` is used throughout for geocentric sidereal
longitudes. This is correct **only when longitude is in [0, 360)**. Always
verify longitude is bound before sign lookup.

### §3.5 — Missing Domain Objects (Required for Roadmap)

The following domain objects are absent and must be created before the
corresponding services can be built:

- `NakshatraPosition` — 27-nakshatra system with pada subdivision
- `GauquelinSector` — diurnal sector (1–36) with angular peak proximity score
- `TransitWindow` — a time range with entering/peak/leaving JDs for a transit
- `CyclePhase` — named synodic phase (new, first quarter, full, last quarter, waning)
- `MarketCycleCorrelation` — astronomical event ↔ financial date pair (no price, just timing)

---

## §4 — API Design Rules

### §4.1 — Response Envelope

Every endpoint MUST return `BaseAstroResponse[T]`:
```python
class BaseAstroResponse[T](BaseModel):
    meta: AstroMeta
    data: T
```

`AstroMeta` must include: `zodiac`, `ayanamsa`, `house_system`,
`coordinate_system`, `calculation_time`. These are non-optional. Callers need
metadata to reproduce identical results.

### §4.2 — No Business Logic in Routers

Routers do exactly three things:
1. Parse and validate the request (Pydantic handles this).
2. Instantiate required services (or receive via DI).
3. Call one service method and return the response.

Any conditional logic, calculation, or data transformation belongs in a service.

### §4.3 — Ephemeris Instantiation Pattern

Currently routers instantiate `Ephemeris()` directly at module level:
```python
ephemeris = Ephemeris()  # module-level in alerts.py, charts.py, etc.
```
This is safe because `Ephemeris` is a singleton. However, the correct pattern
for testability is **FastAPI dependency injection**:

```python
def get_ephemeris() -> Ephemeris:
    return Ephemeris()

@router.get(...)
async def endpoint(eph: Annotated[Ephemeris, Depends(get_ephemeris)]):
    ...
```

Use the DI pattern for all new endpoints to enable mocking in tests.

### §4.4 — Versioning

The API is versioned at `/api/v1/`. All new routes must be in `app/api/v1/`.
When breaking changes are required:
- Create `app/api/v2/` — never modify existing v1 contracts.
- The router prefix in `main.py` must match the directory version.

### §4.5 — HTTP Status Codes

| Scenario | Code |
|---|---|
| Success | 200 |
| Invalid Input | 422 (Pydantic handles this) |
| Unsupported planet/body | 400 |
| Search range exceeded | 400 |
| Ephemeris files missing | 503 |
| Calculation failure | 500 |

Map `AstroError` subclasses to HTTP status codes in a centralized exception
handler registered on `app`:
```python
@app.exception_handler(UnsupportedPlanetError)
async def unsupported_planet(req, exc):
    return JSONResponse(status_code=400, content={"error": str(exc)})
```
Currently there is **no global exception handler** — all errors propagate as 500.
This is a gap.

### §4.6 — Missing Routers (Required for Roadmap)

These service modules exist but have no corresponding router:
- `crossing_service.py` → no `/api/v1/crossings` endpoint
- `panchanga_service.py` → no `/api/v1/vedic/panchanga` path exposed in v1
- `horizon_service.py` → no `/api/v1/horizon` endpoint
- `financial_time_service.py` → stub only, no router
- `sector_engine.py` → no `/api/v1/sectors` endpoint

---

## §5 — Aspect Calculation Rules

### §5.1 — Angular Difference

Use the minimum arc (0–180°) method:
```python
diff = abs(p1.longitude - p2.longitude)
if diff > 180:
    diff = 360 - diff
```
This is correctly implemented. Do not change it.

### §5.2 — Applying/Separating Detection

The current logic in `aspect_service.py` for applying/separating is partially
correct but has edge cases at 0°/360° wrap and exactly-at-aspect conditions.

**Canonical method:**
```
is_applying = True if the angular gap between planets is decreasing
             = relative_velocity × angular_diff < 0
```

Where `angular_diff = (lon2 - lon1 + 180) % 360 - 180` (signed, -180 to +180).

For the opposition (180°), the midpoint-crossing logic currently works only for
the positive half. Verify and add test coverage for the Pisces-Aries zero-point
boundary case.

### §5.3 — Aspect Orbs

Orbs must be adjustable per request. The `DEFAULT_ORBS` in `AspectService` are
project defaults, not rules. Clients may supply `custom_orbs` per aspect type
or a `global_orb` override. This is implemented correctly — preserve it.

### §5.4 — Harmonic Families

The septile angles (`360/7 = 51.4286°`) are stored as truncated floats
(`51.43`). This introduces a ~0.0014° systematic error. Change to:
```python
SEPTILE_ASPECTS = {
    360 / 7: "SEPTILE",
    720 / 7: "BISEPTILE",
    1080 / 7: "TRISEPTILE",
}
```

Same for undecile: use `360/11`, `720/11`, `1080/11` instead of rounded values.

---

## §6 — Time Arithmetic Rules

### §6.1 — The JD Divisor Bug

In `core/time.py`, line 34:
```python
+ dt.second / 84600.0   # WRONG — should be 86400.0
+ dt.microsecond / 84600000000.0  # WRONG — should be 86400000000.0
```
This is a systematic bias. Fix it. After fixing, run the regression test suite
to verify no precision breakage.

### §6.2 — Delta-T

`Time.delta_t` correctly uses `swe.deltat()` which returns days. For very old
or future dates (>3000 CE), Delta-T uncertainty grows rapidly. Document this
limit. Never apply Delta-T correction inside the service layer — it is the
caller's responsibility if ET precision is needed.

### §6.3 — Tropical Year

`ProgressionService` uses `365.242189` days for tropical year in secondary
progressions. This is the correct mean tropical year value. Do not change it.

### §6.4 — Sidereal Year

For sidereal return calculations, use `365.25636` days (Earth's sidereal orbital
period). Do not confuse with the tropical year.

### §6.5 — Synodic Periods (Reference Constants)

| Planet pair | Approximate synodic period |
|---|---|
| Sun–Moon (Lunar) | 29.53059 days |
| Earth–Mercury | 115.88 days |
| Earth–Venus | 583.92 days |
| Earth–Mars | 779.94 days |
| Earth–Jupiter | 398.88 days |
| Earth–Saturn | 378.09 days |

Use these as initial step sizes for bisection searches to avoid missing crossings.
`cycle_service.py` currently uses a fixed 0.5-day step for all planets — this
can miss Mercury which moves ~1.38°/day and has a synodic cycle of only 115 days.

---

## §7 — Performance & Scaling Rules

### §7.1 — The Global Lock is a Bottleneck

`_SWISS_LOCK = RLock()` serializes all ephemeris calls across all threads.
Under concurrent HTTP load, this will become a bottleneck. Mitigation options
(in order of priority):

1. **Async worker pool**: Run all ephemeris calls in `asyncio.get_event_loop().run_in_executor()`
   with a `ThreadPoolExecutor`. This prevents blocking the event loop without
   removing the lock.
2. **Process isolation**: For high-volume deployments, use a dedicated
   ephemeris worker process accessed via a message queue (e.g., Redis + RQ).
3. **Per-request caching**: Cache `calculate_planet(jd, planet)` results keyed
   by `(jd_rounded_to_6dp, planet, flags)` using `functools.lru_cache` or
   `cachetools.TTLCache`. Use 6 decimal places for JD (≈0.086 second precision).

### §7.2 — Scan Operations

Bisection searches (`find_planetary_return`, `scan_ingresses`, etc.) call
`calculate_planet()` 30–50 times per event. For bulk scans over years of data,
this multiplies quickly.

Rules:
- Always validate the range against `MAX_SEARCH_DAYS` (36525 days = 100 years).
- For bulk event scanning, prefer the existing `EventService.scan_ingresses()`
  over `CrossingService.find_ingresses()` — the former is more efficient.
- Never scan within a router — always delegate to a service.

### §7.3 — Background Tasks

The alert scanner (`ScannerService`) is currently synchronous and called via an
HTTP POST. For production:
- Move scanning to a background task: `FastAPI BackgroundTasks` for lightweight
  use, or `Celery` + `Redis` for high-volume scheduled scanning.
- The `financial_time_service.py` stub will need background task execution when
  implemented.

### §7.4 — Database

Currently uses SQLite via SQLModel for alert persistence (`astrosdk.db`).
- SQLite is appropriate for development and single-instance production.
- For multi-process or multi-instance deployments, switch to PostgreSQL.
- Database operations must never block ephemeris calculations — keep them in
  separate async paths.
- The `AlertRule` model is the only ORM model. Keep ORM usage minimal — the SDK
  is not a data warehouse.

---

## §8 — Testing Standards

### §8.1 — Regression Test Requirements

Every astronomical calculation function MUST have at least one regression test
with a known-good value extracted from a validated external source (Astro.com,
JPL Horizons, or printed ephemeris).

Required format:
```python
# REGRESSION: Value sourced from Astro.com for 1990-01-01 12:00 UTC, Lahiri
assert abs(result.longitude - EXPECTED) < TOLERANCE
```

Tolerances:
- Planetary longitude: ≤ 0.001° (3.6 arc-seconds)
- House cusps: ≤ 0.01°
- Eclipse peak JD: ≤ 0.001 JD (≈1.4 minutes)
- Rise/set times: ≤ 0.0007 JD (≈1 minute)

### §8.2 — Test Directory Organization

```
tests/
├── conftest.py               # Shared fixtures (Ephemeris, reference times)
├── regression/               # Golden-value tests, NEVER mocked
├── test_core.py              # Unit tests for Time, Ephemeris, constants
├── test_domain.py            # Unit tests for domain model properties
├── test_aspects_ayanamsas.py # Parameterized across all 47 sidereal modes
├── test_edge_cases.py        # Boundary conditions (polar latitudes, wrap-around)
└── test_api_v1.py            # Integration tests for HTTP endpoints
```

### §8.3 — No Mocking of Ephemeris in Regression Tests

Regression tests MUST use the real `Ephemeris` singleton with real ephemeris
files. Mocking `swisseph` defeats the purpose of regression testing.
Mock only in pure unit tests of non-ephemeris logic (e.g., aspect angle math).

### §8.4 — Test Markers

Use markers defined in `pyproject.toml`:
- `@pytest.mark.slow` — tests taking >5 seconds (e.g., multi-year scans)
- `@pytest.mark.regression` — golden-value tests against known data
- `@pytest.mark.integration` — full HTTP stack tests

### §8.5 — Missing Test Coverage (Gaps)

The following are untested or under-tested as of audit:
- `EphemerisContext` state restoration correctness
- `Time.delta_t` against known values
- Vimshottari Dasha boundary conditions (first Mahadasha remainder)
- Applying/separating in opposition aspects (Pisces↔Aries boundary)
- TransitService `is_applying` (hardcoded `False` — always wrong)
- `scan_aspects()` in `EventService` (method is empty, returns `[]`)
- Eclipse magnitude extraction (hardcoded `1.0`)
- `CycleService.compute_synodic_cycle()` (returns empty list `[]`)

---

## §9 — Vedic-Specific Rules

### §9.1 — Ayanamsa Requirement

All Vedic calculations (Vargas, Dashas, Panchanga, Nakshatra) MUST use a
sidereal mode. The default is `LAHIRI`. Passing `sidereal_mode=None` in a
Vedic context is an error and must raise `ConfigurationError`.

### §9.2 — Vimshottari Dasha

The total cycle is 120 years. The sequence of lords and their years:
Ketu(7), Venus(20), Sun(6), Moon(10), Mars(7), Rahu(18), Jupiter(16), Saturn(19), Mercury(17).
Sum = 120. This is hardcoded correctly in `VedicService.DASHA_LORDS`.

The starting lord is determined by the Moon's nakshatra at birth:
- 27 nakshatras map to 9 lords (3 nakshatras per lord).
- `nak_idx % 9` gives the starting lord index. This is correct.
- The first dasha's remaining duration = `rem_nak × full_dasha_years`.

### §9.3 — Navamsa (D9) Calculation

The current Navamsa implementation uses a `cycle_starts = [0, 9, 6, 3]` lookup
based on `sign_idx % 4`. This represents the traditional fire/earth/air/water
triplicity sub-cycle. Verify accuracy against a reference Navamsa table for
at least 3 known birth charts before trusting production outputs.

### §9.4 — Panchanga Accuracy

- **Tithi**: `(moon_lon - sun_lon) % 360 / 12`. This is correct.
- **Yoga**: `(sun_lon + moon_lon) % 360 / (360/27)`. This is correct.
- **Karana**: `diff / 6`. Index wraps with `% 11` for the 7 recurring karanas.
  The 4 fixed karanas (Shakuni, Chatushpada, Naga, Kinstughna) occur on specific
  tithis only — the current implementation treats all karanas as equally recurring,
  which is astronomically incorrect for Amavasya and full-moon tithis.

### §9.5 — Missing Vedic Modules

- **Shadbala** (planetary strength calculation) — not implemented
- **Ashtakavarga** — not implemented
- **Shodashavarga** (D60, D24, etc.) — only D9 has custom logic; others use
  generic proportional multiplication which is incorrect for odd divisions
- **Yoga detectors** (Raj Yoga, Dhana Yoga, etc.) — not in scope per SDK mandate
  (interpretation-free), but the underlying conjunction/house data is available

---

## §10 — Financial Astrology Rules

### §10.1 — Boundary of Responsibility

The SDK provides **astronomical timing data only**. It does NOT:
- Predict price direction
- Generate buy/sell signals
- Estimate volatility
- Correlate astronomical events with market returns

Any output from `quant_service.py` or `financial_time_service.py` is raw
astronomical timing, not a trading recommendation.

### §10.2 — Gann Price Mapping

`gann_price_mapping(longitude, scale=1.0)` returns `longitude × scale`. This
is a valid implementation of the W.D. Gann degrees-to-price concept. It must
never claim predictive validity — it is a transformation, not a forecast.

### §10.3 — Synodic Phase

`calculate_synodic_phase(p1, p2, time)` returns the phase angle (0–360°)
of p2 relative to p1. Phase 0 = conjunction (new cycle start). This is the
correct astronomical interpretation. The `is_waxing` flag (`phase < 180`) is
correct.

### §10.4 — Velocity ROC

Velocity Rate of Change is a second-order derivative: `(v_now - v_prev) / window_days`.
The reference average speeds in `quant_service.py` are correct approximations.
Flag calculations that use `window_days=1.0` as the only choice — expose this
as a configurable parameter with validation (`0.1 ≤ window_days ≤ 30`).

### §10.5 — Missing Financial Modules (Roadmap)

- **Ephemeris export** (bulk JD-indexed CSV of planetary positions) — the most
  requested financial use-case; critical for backtesting
- **Synodic cycle completion scanner** (find all conjunctions between two bodies
  over a time range)
- **Heliocentric position export** — currently supported in calculations but no
  dedicated bulk export endpoint
- **CycleService.compute_synodic_cycle()** is stubbed — must return all new,
  quarter, full, and last-quarter phases between two planets over a range

---

## §11 — Anti-Patterns to Avoid

### §11.1 — Swisseph Direct Calls Outside Ephemeris

**NEVER do this:**
```python
# In any service, router, or domain file:
import swisseph as swe
result = swe.calc_ut(jd, planet, flags)  # Not thread-safe!
```

Only `app/core/ephemeris.py` may call `swe.*` directly.

**Exception**: `EphemerisContext` and `Time` may call `swe.set_*`, `swe.sidtime`,
and `swe.deltat` because they are architectural extensions of the core layer.
Even so, context calls must hold `_SWISS_LOCK` or be within a locked block.

**Violation found**: `event_service.py` lines 227–232 call `swe.rise_trans`
directly. This must be refactored to use `Ephemeris.calculate_rise_set()`.

### §11.2 — Generic Exception Swallowing

**NEVER do this:**
```python
try:
    result = some_calculation()
except Exception:
    break  # or pass, or return None
```

Found in `crossing_service.py` line 185: `except Exception: break`. Log the
exception and surface it. Silent failures in astronomical scans will produce
incomplete results with no indication to the caller.

### §11.3 — Hardcoded Constants in Services

**NEVER:**
```python
# in quant_service.py
average_speeds = {Planet.SUN: 0.9856, ...}  # embedded in service method
```

Move physical constants to `core/constants.py`. Services should reference
constants, not define them.

### §11.4 — String Types Where Enum Types Should Be Used

**NEVER:**
```python
AstroEvent(type="INGRESS", ...)  # "type" should be AstroEventType.INGRESS
```

All categorical fields in domain objects must be enums. Strings allow typos
that fail at runtime, not at definition time.

### §11.5 — Mutable Default Arguments

**NEVER:**
```python
def calculate(planets: list[Planet] = [])  # shared mutable default
```

Use `None` with explicit check inside the function.

### §11.6 — Module-Level Singleton Creation in Routers

While `Ephemeris()` is a singleton and therefore safe, creating
service objects at module level (not inside route handlers or DI providers)
makes unit testing impossible without monkey-patching. Always use DI:

```python
# Bad
service = SomeService(Ephemeris())

# Good
def get_service() -> SomeService:
    return SomeService(Ephemeris())
```

### §11.7 — Magic Numbers

**NEVER:**
```python
max_safety = 50  # in crossing_service.py
```

Extract to a named constant with documentation:
```python
MAX_INGRESS_SCAN_ITERATIONS = 50  # Safety limit for find_ingresses() loop
```

### §11.8 — Missing Return Type Annotations

All functions must have complete type annotations. Run `mypy --strict` and fix
all violations before merging. The CI pipeline must reject any code that fails
`mypy --strict`.

### §11.9 — Unimplemented Stubs Left in Production Code

**NEVER** leave a method returning `[]` or `pass` in production:
```python
def compute_synodic_cycle(self, ...) -> list[CycleEvent]:
    # ...
    return []  # NOT IMPLEMENTED
```

Either implement it, raise `NotImplementedError`, or remove it. Empty stubs
mislead callers into thinking results were computed.

### §11.10 — Non-UTC Timezone Handling

**NEVER:**
```python
datetime.now()  # naive, timezone-free
```

Always use:
```python
datetime.now(UTC)  # explicit UTC
```

---

## §12 — Code Quality Requirements

| Tool | Configuration | Requirement |
|---|---|---|
| `mypy` | `strict = true` | Zero violations |
| `ruff` | See `[tool.ruff]` | Zero violations |
| `pytest` | `--strict-markers` | 100% pass rate |
| Coverage | `pytest-cov` | ≥ 90% line coverage for `core/` and `services/` |

Run before every commit:
```bash
ruff check app/ tests/
mypy app/
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## §13 — Dependency Rules

Allowed dependencies (from `pyproject.toml`):
- `pyswisseph` — Swiss Ephemeris bindings (core)
- `fastapi` + `uvicorn` — HTTP framework
- `pydantic` — request/response validation
- `sqlmodel` — ORM for alert persistence
- `python-dotenv` — environment config
- `tzdata` — timezone database
- `numpy` + `pandas` — numerical/tabular output for quant endpoints
- `matplotlib` — chart visualization (quant only, optional)

**Prohibited:**
- No ML/AI libraries (`scikit-learn`, `tensorflow`, etc.)
- No financial data providers (`yfinance`, `alpaca`, `ccxt`, etc.)
- No interpretation engines
- No web scraping libraries
- No new ORM layers (stay on SQLModel)

---

## §14 — Roadmap Alignment

Implement features in this priority order, never skipping phases:

### Phase 1 — Core Hardening (Current)
- [ ] Fix `Time._to_jd()` divisor bug (84600 → 86400)
- [ ] Fix eclipse magnitude extraction (hardcoded 1.0)
- [ ] Fix `scan_aspects()` empty stub in EventService
- [ ] Fix `compute_synodic_cycle()` empty stub in CycleService
- [ ] Fix direct `swe.*` calls in `event_service.py`
- [ ] Replace all string event types with `AstroEventType` enum
- [ ] Add global exception handlers for all `AstroError` subclasses
- [ ] Fix Karana fixed-karana boundary conditions in PanchangaService
- [ ] Fix `EphemerisContext` to save/restore previous sidereal mode
- [ ] Fix septile/undecile angle precision (use rational fractions)

### Phase 2 — API Completeness
- [ ] Add `/api/v1/crossings` router
- [ ] Add `/api/v1/horizon` router
- [ ] Add `/api/v1/sectors` router
- [ ] Expose panchanga as `/api/v1/vedic/panchanga`
- [ ] Ephemeris DI pattern for all routers
- [ ] Centralized error handler registration in `main.py`

### Phase 3 — Scaling & Quant
- [ ] Async executor wrapper for all `Ephemeris` calls
- [ ] `CycleService.compute_synodic_cycle()` — full implementation
- [ ] Bulk ephemeris export endpoint (CSV, JD-indexed)
- [ ] Velocity ROC configurable window parameter
- [ ] Background task architecture for `ScannerService`

### Phase 4 — Financial Astrology Layer
- [ ] Heliocentric position bulk export
- [ ] Synodic conjunction scanner (all conjunctions over a range)
- [ ] `MarketCycleCorrelation` domain object and service
- [ ] Optional PostgreSQL migration path

### Phase 5 — Vedic Completeness
- [ ] Shadbala calculation service
- [ ] Shodashavarga (D1–D60) with correct algorithms per division
- [ ] Ashtakavarga service
- [ ] Pratyantardasha (Level 3 Dasha)

---

*This file is the single source of truth for all engineering and domain decisions in the AstroSDK project. AI agents must read this file in full before making any changes to the codebase.*
