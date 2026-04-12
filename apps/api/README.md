# AstroSDK 2.0: Professional Astrology Engine

AstroSDK 2.0 is a deterministic, professional-grade astronomical calculation engine designed for research, financial astrology, and enterprise applications. Built on the Swiss Ephemeris and NASA JPL data, it provides sub-arc-second precision with a modern, context-aware architecture.

## 🚀 2.0 Key Features

- **Service-First Architecture**: Use the core engine directly via Python Services or through the high-performance FastAPI V2 namespace.
- **Context-Aware Determinism**: Every calculation is governed by a `CalculationContext`, ensuring results are reproducible across any environment.
- **Surface Geometry**: Native support for **Topocentric** (observer-based) and **Heliocentric** (Sun-centered) coordinate systems.
- **Global Precision**: Verified against NASA JPL DE431/DE432 ephemeris files.

## 🛠 Installation

```bash
pip install -r requirements.txt
pip install -e .
```

Requires high-precision ephemeris data path to be set via `SE_EPHE_PATH` environment variable.

## 🚦 Quickstart (Python Service)

```python
from app.services.astronomy.planetary_service import AstronomyPlanetaryService
from app.contexts.factories import create_default_context
from app.core.time import Time
from datetime import datetime

# 1. Build context
ctx = create_default_context()
ctx.coordinate.system = "topocentric"
ctx.observer.latitude = 51.5074  # London
ctx.observer.longitude = -0.1278

# 2. Run high-precision service
time = Time(datetime.now())
service = AstronomyPlanetaryService(ctx)
positions = service.calculate_positions(time) 
```

## 🎯 Development Status

- [x] **Natal/Transit Core**: High-precision calculation engine (2.0)
- [x] **Vedic Hub**: Panchanga and Yoga elements (2.0)
- [x] **Research Layer**: Financial, Mundane, and Quant signals (2.0) - **GRADUATED**
- [ ] **ML Bridge**: Feature extraction for predictive modeling (In-Progress)

## 📖 Documentation

- [API Reference](docs/API_REFERENCE.md) - Context-aware endpoints and header spec.
- [Practical Examples](docs/EXAMPLES_2.0.md) - Common cURL scenarios for 2.0.
- [Walkthrough & Verification](walkthrough.md) - Deep dive into 2.0 graduation.

## 🧪 Testing

AstroSDK 2.0 maintains 100% verification for core astronomical benchmarks.

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/regression/test_data_integrity.py -v
pytest tests/api/test_v2_smoke.py -v
```
