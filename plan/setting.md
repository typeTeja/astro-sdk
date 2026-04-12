Implement Astrology Settings (Backend)

````text id="astro-settings-impl"}
You are a Senior Backend Engineer building a high-precision Astrology API using FastAPI, Pydantic v2, and Swiss Ephemeris.

Your task is to implement a robust, extensible "Astrology Settings" system that controls ALL calculation behavior.

---

## 🧠 Core Principles (MUST FOLLOW)

1. Deterministic outputs:
   - Same input → same output
   - No hidden defaults
   - No system time usage

2. Explicit configuration:
   - ALL calculation settings must be passed explicitly or resolved via a validated config object

3. Separation of concerns:
   - Routes → validation only
   - Services/Domain → calculations

4. Backend is the single source of truth:
   - Frontend must NOT decide astrology logic

5. No astrology logic in routes

---

## 🎯 Goal

Design and implement a reusable **ChartSettings system** that:

- Controls zodiac, ayanamsa, houses, nodes, etc.
- Is reusable across:
  - natal
  - transits
  - panchanga
  - financial modules (future)

---

## 🧱 Step 1: Define Settings Model

Create:

`app/schemas/settings.py`

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class ChartSettings(BaseModel):
    zodiac: Literal["sidereal", "tropical"] = "sidereal"

    ayanamsa: Optional[
        Literal["lahiri", "raman", "kp", "yukteshwar", "fagan"]
    ] = "lahiri"

    house_system: Literal[
        "whole_sign", "placidus", "koch", "equal", "kp"
    ] = "whole_sign"

    node_type: Literal["true", "mean"] = "true"

    coordinate_system: Literal[
        "geocentric", "heliocentric", "topocentric"
    ] = "geocentric"

    planets: Optional[List[str]] = None  # optional filtering

    include_outer_planets: bool = False

    aspect_system: Optional[Literal["vedic", "western"]] = None

    orb: Optional[float] = Field(default=None, ge=0, le=10)

    class Config:
        extra = "forbid"
````

---

## 🧱 Step 2: Create Resolver Layer (IMPORTANT)

Create:

`app/core/settings_resolver.py`

Purpose:

* Validate combinations
* Enforce rules
* Normalize defaults

```python
def resolve_settings(settings: ChartSettings) -> ChartSettings:
    # Example rule:
    if settings.zodiac == "tropical":
        settings.ayanamsa = None

    if settings.zodiac == "sidereal" and not settings.ayanamsa:
        raise ValueError("Ayanamsa required for sidereal zodiac")

    return settings
```

---

## 🧱 Step 3: Integrate into Request Model

Update:

`schemas/requests.py`

```python
class NatalChartRequest(BaseModel):
    date: date
    time: time
    timezone: str
    latitude: float
    longitude: float

    settings: ChartSettings
```

---

## 🧱 Step 4: Dependency Injection (Clean Architecture)

Create:

`api/deps.py`

```python
from fastapi import Depends

def get_settings(
    settings: ChartSettings
) -> ChartSettings:
    return resolve_settings(settings)
```

---

## 🧱 Step 5: Use in Route (Thin Controller)

```python
@router.post("/natal")
def get_natal_chart(
    request: NatalChartRequest,
):
    settings = resolve_settings(request.settings)

    return natal_chart_service.generate_chart(
        request,
        settings
    )
```

---

## 🧱 Step 6: Pass to Service Layer

```python
def generate_chart(data, settings: ChartSettings):
    # NEVER hardcode zodiac/ayanamsa
    # ALWAYS use settings

    if settings.zodiac == "sidereal":
        apply_ayanamsa(settings.ayanamsa)

    houses = calculate_houses(settings.house_system)

    nodes = calculate_nodes(settings.node_type)

    ...
```

---

## 🧱 Step 7: Swiss Ephemeris Integration

Ensure:

* sidereal vs tropical explicitly set
* ayanamsa explicitly applied
* no silent switching

---

## 🧱 Step 8: Validation Rules (STRICT)

Enforce:

* zodiac = tropical → ayanamsa must be None
* orb only valid if aspect_system exists
* planets list must be valid enum
* no unknown fields

---

## 🧱 Step 9: OpenAPI Contract

Ensure:

* Settings appear in request schema
* Defaults are visible
* Fully typed enums

---

## 🧱 Step 10: Testing (MANDATORY)

Write tests:

* settings resolution
* sidereal vs tropical behavior
* invalid combinations
* deterministic outputs

---

## 🚫 Forbidden

* Hardcoded astrology values
* Implicit defaults inside services
* Mixing tropical/sidereal silently
* Any astrology logic in routes

---

## ✅ Output Required

1. settings.py model (check any exsting setting model in the project and update it)
2. resolver.py logic (check any exsting resolver logic in the project and update it)
3. updated request schema (check any exsting request schema in the project and update it)
4. service integration example 
5. 3–5 validation tests 
---

## 🧠 Philosophy Reminder

This settings system is:

* The control layer of the entire astrology engine
* Must be explicit, testable, and future-proof

You are NOT building UI settings.

You are building:
→ A deterministic configuration system for a scientific astrology engine

