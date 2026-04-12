# 🚀 AstroSDK 2.0: Practical Examples

This guide provides copy-pasteable examples for common 2.0 scenarios.

## ⚙️ Overriding Calculation Context
You can use headers to force any endpoint into a specific zodiac or coordinate system.

### Request Sidereal Lahiri Chart
```bash
curl -X GET "http://localhost:8000/api/v2/charts/panchanga?latitude=18.97&longitude=72.82" \
     -H "X-Astro-Is-Sidereal: true" \
     -H "X-Astro-Sidereal-Mode: LAHIRI"
```

---

## 📅 Financial & Mundane Scanning

### Find Mercury Retrograde Windows (2024)
```bash
curl -X GET "http://localhost:8000/api/v2/financial/windows?planets=MERCURY&start_time=2024-01-01&end_time=2024-12-31"
```

### Get Synodic Phase between Jupiter and Saturn
```bash
curl -X GET "http://localhost:8000/api/v2/quant/synodic/phase?p1=JUPITER&p2=SATURN"
```

---

## 📈 Quantitative Signals

### Get Global Astro-Intensity (Next 30 Days)
```bash
curl -X GET "http://localhost:8000/api/v2/signals/astro-intensity?max_days=30"
```

### Find Clusters (Stelliums) in the Sky
```bash
curl -X GET "http://localhost:8000/api/v2/signals/cluster-index?orb_degrees=8.0"
```

---

## 🔭 Astronomy & Visibility

### Get Heliacal Rising of Venus
```bash
curl -X GET "http://localhost:8000/api/v2/heliacal/rising?planet=VENUS&latitude=40.71&longitude=-74.00"
```

### High-Precision Planet Position (Heliocentric)
```bash
curl -X GET "http://localhost:8000/api/v2/astronomy/planet-position?planet=MARS" \
     -H "X-Astro-Coordinate-System: heliocentric"
```
