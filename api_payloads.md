# AstroSDK Endpoint Payload Cheat Sheet

This guide provides exactly what your Next.js application needs to send via Axios (or Fetch) to generate mathematically perfect responses from the backend engine.

---

## 1. Core Charting Requests
**Endpoints:** `/api/v1/charts/geocentric`, `/api/v1/charts/topocentric`, `/api/v1/charts/heliocentric`

These are the primary workhorses for calculating planet arrays.

```json
{
  "time": {
    "time": "2024-04-08T18:00:00Z"
  },
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "altitude": 0
  },
  "settings": {
    "sidereal_mode": "LAHIRI",
    "house_system": "WHOLE_SIGN",
    "is_sidereal": true
  }
}
```

---

## 2. Temporal & Basic Requests
**Endpoints:** `/api/v1/events/phenomena`, `/api/v1/lunar/phases`, `/api/v1/nodes/lunar`, `/api/v1/synodic/cycles`, `/api/v1/financial/eclipses`, `/api/v1/financial/retrogrades`

When you only need a single point in time to scan global phenomena (no location needed).

```json
{
  "time": "2024-04-08T18:00:00Z"
}
```

---

## 3. Transits & Progressions Additions
**Endpoints:** 
- `POST /api/v1/transits/scan?transit_time=2024-04-08T18:00:00Z`
- `POST /api/v1/transits/helion?transit_time=2024-04-08T18:00:00Z`
- `POST /api/v1/transits/declination?transit_time=2024-04-08T18:00:00Z`
- `POST /api/v1/progressions/secondary?target_date=2025-01-01T00:00:00Z`

Transits use the base `NatalChartRequest` as the body (representing the native's birth chart) and pass the transit evaluation time as **URL Query Parameters**.

```json
// POST Body (Native Chart)
{
  "time": { "time": "1990-05-15T12:00:00Z" },
  "location": { "latitude": 34.0522, "longitude": -118.2437, "altitude": 0 }
}
```

---

## 4. Deep Vedic Endpoints
**Endpoints:** 
- `POST /api/v1/vedic/divisional?division=9`
- `POST /api/v1/vedic/dashas?levels=3`
- `POST /api/v1/vedic/shadbala`
- `POST /api/v1/vedic/ashtakavarga`

All of these rely on the Native's foundation geometry. Send the standard Chart Payload (`time` & `location`) with query params directing the depth of the algorithm.

```json
// POST Body
{
  "time": { "time": "1990-05-15T12:00:00Z" },
  "location": { "latitude": 34.0522, "longitude": -118.2437, "altitude": 0 },
  "settings": { "is_sidereal": true, "sidereal_mode": "LAHIRI" }
}
```

---

## 5. Webhook Alerts System
**Endpoint:** `POST /api/v1/alerts/rules`

Used to establish permanent autonomous triggers in the system database.

```json
{
  "name": "Market Crash Mars Return",
  "planet": "MARS",
  "secondary_planet": "SATURN",
  "event_type": "ASPECT",
  "target_value": 90.0,
  "webhook_url": "https://api.yournextjsapp.com/webhooks/astro",
  "is_active": true
}
```

Then hook into your scheduler by submitting:
`POST /api/v1/alerts/scan?window_days=7.0&background=true`

---

## 6. Composite Engines 
**Endpoint:** `POST /api/v1/cycles/composite`

Mashes multiple distinct charts into a single unified temporal centroid.

```json
{
  "charts": [
    {
      "time": { "time": "1990-01-01T12:00:00Z" },
      "location": { "latitude": 40.71, "longitude": -74.00, "altitude": 0 }
    },
    {
      "time": { "time": "1995-05-05T12:00:00Z" },
      "location": { "latitude": 34.05, "longitude": -118.24, "altitude": 0 }
    }
  ],
  "settings": {}
}
```

---

## 7. Deep Research & Machine Learning Export
**Endpoints:** 
- `POST /api/v1/research/astro-scan`
- `POST /api/v1/research/event-frequency`
- `POST /api/v1/research/astro-dataset`
- `POST /api/v1/research/csv`

Built specifically for scraping longitudinal bounds for ML modeling.
```json
{
  "start_time": "2020-01-01T00:00:00Z",
  "end_time": "2030-01-01T00:00:00Z",
  "step_days": 1.0,
  "planets": ["SUN", "JUPITER", "SATURN"],
  "location": { "latitude": 0, "longitude": 0, "altitude": 0 }
}
```

---

## 8. Statistics & Market Signals
**Endpoints:**
- `POST /api/v1/signals/cluster-index`
- `POST /api/v1/signals/intensity`
- `POST /api/v1/quant/synodic-phases`

Evaluates system-wide gravitational densities. Send a standard universal time reference.
```json
{
  "time": "2024-06-15T12:00:00Z"
}
```

---

## 9. Parans & Fixed Stars
**Endpoints:** 
- `POST /api/v1/stars/scan`
- `POST /api/v1/parans/scan`

Looks for Deep-Sky intersections specifically pinned to the native's birth location geometry.
```json
{
  "time": { "time": "1990-05-15T12:00:00Z" },
  "location": { "latitude": 34.0522, "longitude": -118.2437, "altitude": 0 }
}
```

---

## 10. Abstract Geometries (Nodes & Projections)
**Endpoints:** 
- `POST /api/v1/nodes/lunar`
- `POST /api/v1/nodes/planetary`
- `POST /api/v1/nodes/apsides` (Lilith/Priapus, Perihelions)
- `POST /api/v1/projections/time-swing`
- `POST /api/v1/projections/synodical-line`

`Nodes` accept a standard temporal `AstroInput` (just timestamp).
`Projections` accept the standard `NatalChartRequest`, analyzing geometric vectors originating from the base chart points dynamically.

---

## 11. Configuration Echo & Health
**Endpoints:** 
- `GET /api/v1/astro/ephemeris-status` (No payload)
- `GET /version` (No payload)
- `GET /` (No payload, root health proxy)
- `POST /api/v1/astro/settings`

Used to rapidly validate custom client configurations without breaking the isolated state rule in production.
```json
{
  "sidereal_mode": "FAGAN_BRADLEY",
  "house_system": "PLACIDUS",
  "is_sidereal": true
}
```
