# 🌌 ASTRO SDK – REQUIRED FEATURE SPECIFICATION

---

# 1️⃣ Astronomical Core Engine (High-Precision)

### Planetary Computation

* Geocentric positions
* Longitude & latitude
* Speed & acceleration
* Retrograde flag
* True & Mean Node support
* Delta-T handling
* UT ↔ Julian Day conversion (centralized)
* Reproducible Julian Day calculation
* No `now()` inside core

### Zodiac & Coordinate Configuration

* Explicit zodiac system (Sidereal default)
* Ayanamsa system (Lahiri default)
* Overrideable zodiac & ayanamsa parameters

---

# 2️⃣ Deterministic Time Engine

### Input Requirements

* Explicit date
* Explicit time
* Explicit timezone
* Timezone validation

### Internal Handling

* Strict UTC normalization
* Central time utility module
* Deterministic time conversion
* Identical input → identical output

---

# 3️⃣ Natal Chart Engine

### Angles & Houses

* Ascendant (correct house cusp mathematics)
* MC / IC
* Whole Sign (default)
* Placidus
* Koch
* Equal
* KP
* Support for all supported house systems

### Planetary States

* Retrograde status
* Planet combust status
* Graha dignities (structured, optional)

### Output Requirements

* Deterministic output schema
* Structured data only (no interpretation text)

---

# 4️⃣ Aspect Engine

### Core Aspect Support

* All aspects
* Configurable orb
* Applying / separating detection
* Exact aspect perfection timestamp
* Exact timestamp search
* Event range scanning

---

# 5️⃣ Transit Engine

### Transit Modes

* Transit-to-natal aspects
* Transit-to-transit aspects
* Orb filtering
* Time range scanning
* Declination parallels
* Structured output only (no interpretation)

---

# 6️⃣ Event Detection Engine

Must detect and timestamp:

* Ingresses (sign changes)
* Retrograde start / end
* Stations
* Eclipses
* Lunations (New / Full Moon)
* Exact aspect perfection

Returns timestamps and duration windows only.

---

# 7️⃣ Cycle Engine

### Core Cycle Features

* Synodic cycles
* Planet orbital cycles
* Phase % calculation
* Angle returns
* Repetition detection

Pure cycle mathematics.
No forecasting logic.

---

# 8️⃣ Custom Event Rule Engine (Infrastructure-Level Feature)

Critical for advanced users.

### Must Allow JSON-defined Rules:

* Speed < X
* Aspect within orb
* Planet in sign
* Latitude extreme
* Composite condition sets

### Behavior

* Accept structured JSON
* Scan time range
* Return timestamps only
* No interpretation
* No financial advice

This transforms the SDK from a tool → into programmable infrastructure.

---

# 9️⃣ Astro-Intensity Signal Engine

Normalized signal based on:

* Aspect density
* Retrograde overlap
* Eclipse proximity
* Planet clustering

Output:

* Timestamp
* Normalized intensity value
* Structural drivers list
* No direction, no prediction

---

# 1️⃣2️⃣ Ephemeris Export

* Daily / hourly resolution
* Multi-planet support
* CSV / JSON formats
* Research-ready structure

---

# 🏗 Architecture Requirements (Non-Negotiable)

### Layer Discipline

* Routes ≠ Calculations
* Domain layer is pure
* Services orchestrate
* Pydantic models everywhere
* No raw dict passing

### Engineering Standards

* High-precision planetary engine
* Deterministic time handling
* Full regression test suite

---

# ✅ Complete Capability Checklist

Your SDK must include:

* High-precision planetary engine
* Deterministic time handling
* Full natal chart engine
* Aspect search engine
* Transit engine
* Event detection engine
* Cycle engine
* Custom event rule engine
* Astro-intensity signals
* Ephemeris export
* Strict layered architecture
* Full regression test suite


map this features against current SDK and show missing gaps.
