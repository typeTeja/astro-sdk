# AstroSDK 2.0 API Reference

This document provides a technical overview of the V2 API endpoints.

## ⚙️ Calculation Context

Every V2 endpoint respects the `CalculationContext` header pattern. You can override engine settings using these headers:

| Header | Values | Description |
| :--- | :--- | :--- |
| `X-Astro-Is-Sidereal` | `true`, `false` | Enable/Disable Ayanamsa |
| `X-Astro-Sidereal-Mode` | `LAHIRI`, `FAGAN_BRADLEY`, etc. | Select Ayanamsa system |
| `X-Astro-Coordinate-System` | `geocentric`, `topocentric`, `heliocentric` | Set geometry origin |
| `X-Astro-House-System` | `P`, `W`, `K`, `V`, etc. | Select house division system |

> [!WARNING]
> **Strict Coordinate Enforcement**
> If `X-Astro-Coordinate-System` is set to `topocentric`, you **must** provide `latitude` and `longitude` (via headers or query params). Failure to do so will result in a **400 Bad Request** error. Fallback to geocentric is not permitted for topocentric requests.

---

## 🌌 Astronomy Hub (`/api/v2/astronomy`)

### `GET /planet-position`
Returns high-precision coordinates for a single planet.

**Parameters:**
- `planet` (string): e.g., "SUN", "MOON", "MARS"
- `time` (ISO8601): e.g., "2024-04-08T18:00:00Z"
- `latitude` (float): Required for topocentric.
- `longitude` (float): Required for topocentric.

---

## 🎨 Chart Services (`/api/v2/charts`)

### `POST /natal`
Generates a complete natal snapshot including planets, houses, and axes.

**Request Schema:**
```json
{
  "time": {"time": "..."},
  "location": {"latitude": 0, "longitude": 0, "altitude": 0},
  "settings": {"house_system": "P", "is_sidereal": true}
}
```

### `GET /panchanga`
Fast retrieval of the five Vedic elements.

---

## 📐 Aspects (`/api/v2/aspects`)

### `GET /calculate`
Scans for angular interactions between active planets.

**Parameters:**
- `planets` (list): e.g., `SUN`, `MOON`
- `aspect_types` (list): Optional filter, e.g., `CONJUNCTION`, `OPPOSITION`
- `global_orb` (float): Optional override for all aspect orbs.

---

---

## 📈 Research & Financial (`/api/v2/research`)
Astro-financial and quantitative signals for systemic analysis.

### `GET /financial/windows`
Scans for time windows of planetary phases (Retrogrades, Shadow, etc.).
- `planets`: Optional filter for specific bodies.
- `start_time`: Analysis window start.
- `end_time`: Analysis window end.

### `GET /quant/synodic/phase`
Returns current relative longitude and applying/separating status between two planets.
- `p1`, `p2`: The two bodies to compare.

### `GET /signals/astro-intensity`
Quantitative score based on the density of exact aspects in the period.
- `max_days`: Forecast horizon.
- `step_hours`: Series resolution.

---

## 🕒 Mundane Events (`/api/v2/events`)
Tracking high-level global astronomical shift points.

### `GET /events/ingresses`
Find exact times of sign crossings for a planet.
- `planet`: The body to scan.
- `zodiac`: Respects `X-Astro-Is-Sidereal`.

### `GET /events/retrogrades`
Find exact times of stationary points (turning RX or Direct).

---

## 🔭 Visibility & Heliacal (`/api/v2/heliacal`)
Tracking heliacal phenomena and visibility stages.

### `GET /heliacal/rising`
Calculates the first morning visibility of a planet/star after solar conjunction.

---

## 🛠 Stability and Maturity
AstroSDK 2.0 endpoints return a `maturity` level in the metadata:
- `PRODUCTION`: Zero-error-tolerance, production-certified.
- `BETA`: Feature-complete, awaiting final verification.
- `EXPERIMENTAL`: Research-only, subject to change.
