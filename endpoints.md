# 🌌 AstroSDK – API Endpoints List

## 🪐 1. Core Astronomy

### Planetary Data

* `GET /astro/planets/positions`
* `GET /astro/planets/speed`
* `GET /astro/planets/retrograde`
* `GET /astro/planets/latitude`
* `GET /astro/planets/declination`
* `GET /astro/planets/sign`
* `GET /astro/planets/decan`

---

## 🔗 2. Aspects & Angles

* `GET /astro/aspects`
* `GET /astro/aspects/returns`
* `GET /astro/angular-difference`

---

## 🌙 3. Lunar & Eclipse

* `GET /lunar/phases`
* `GET /lunar/eclipses`
* `GET /lunar/apogee-perigee`

---

## 🏠 4. Charts (Core Astrology)

### Natal

* `POST /charts/natal`

### Transit

* `POST /charts/transit`

### Panchanga

* `GET /charts/panchanga`

---

## 🔄 5. Transits & Progressions

* `POST /transits/natal`
* `GET /transits/helion`
* `GET /transits/declination`
* `POST /progressions/secondary`
* `GET /progressions/aspects`

---

## 🔁 6. Cycles & Synodic

* `GET /cycles/planetary`
* `GET /cycles/synodic`
* `GET /cycles/lunar`
* `GET /cycles/angle-returns`
* `GET /cycles/time-by-degree`
* `GET /cycles/time-by-synodic-degree`

---

## 📡 7. Events Engine

* `GET /events/planetary`
* `GET /events/ingresses`
* `GET /events/retrogrades`
* `GET /events/eclipses`

---

## 🧠 8. Custom Event Engine (ULE)

* `POST /events/rules`
* `POST /events/scan`
* `POST /events/custom`

---

## 📈 9. Financial Astrology (Safe)

* `GET /financial/events`
* `GET /financial/time-windows`
* `GET /financial/retrogrades`
* `GET /financial/ingresses`
* `GET /financial/eclipses`

---

## 📊 10. Signals (Non-Predictive)

* `GET /signals/astro-intensity`
* `GET /signals/cluster-index`

---

## 🔮 11. Projections (Time-Based Only)

* `GET /projections/time-swing`
* `GET /projections/synodical-lines`

---

## 📊 12. Research & Data Export

* `GET /ephemeris`
* `POST /research/astro-scan`
* `GET /research/astro-events`
* `GET /research/event-frequency`
* `GET /research/astro-dataset`

---

## 🧩 13. Composite & Advanced Models

* `POST /cycles/composite`

---

## 🔔 14. Alerts & Automation

* `POST /alerts/astro`
* `GET /alerts`
* `DELETE /alerts/{id}`

---

## ⚙️ 15. System & Configuration

* `GET /astro/settings`
* `POST /astro/settings`
* `GET /health`
* `GET /version`

---

# 🧭 Suggested Versioning

All endpoints should be under:

```
/api/v1/...
```

Example:

```
GET /api/v1/astro/planets/positions
```

# ✅ One-Line Summary

👉 **“Complete, modular, API-first astrology engine with zero prediction and full extensibility.”**
