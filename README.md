# AstroSDK 

**Enterprise-Scale Deterministic Astrology API Platform**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AstroSDK is a massive, production-grade REST API backend built on top of the deterministic **Swiss Ephemeris** C-bindings. Originally an isolated SDK, it has been scaled into a **high-concurrency FastAPI stateless microservice** designed exclusively for Data Science, Financial Time-Intelligence scanning, and deeply precise astrological research.

---

## 🎯 Architecture Philosophy

**This API engine is strict infrastructure.**

- **Stateless & Deterministic** - Same input payload always guarantees identical multi-layered JSON generation.
- **REST-First Extensibility** - Exposes over 18 core modular routing tables for everything from granular Helion transits to Deep Vedic matrix scoring.
- **Data over Interpretation** - The engine processes pure geometrical offsets, time-swings, phase clusters, and orbital dynamics. It does *not* generate NLP descriptions or subjective predictions.

---

## ⚠️ Financial Compliance

> **[IMPORTANT] ASTRO-FINANCIAL DOMAIN RESTRICTIONS** 
> 
> The AstroSDK engine strictly calculates astronomical points of interest (Eclipses, Ingresses, Synodic alignments). **It does NOT provide financial advisory, prediction models, or buy/sell signals.** All dedicated financial endpoints enforce a mandatory `no_financial_advice: true` meta-block wrapping their payloads to maintain clean structural and legal boundaries.

---

## 🚀 Quick Start

### Installation

Ensure `pyswisseph` and `FastAPI` dependencies are active.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Launching the Enterprise Server

AstroSDK uses `uvicorn` to mount the monolithic router schema.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Browse to `http://localhost:8000/docs` to visualize the massive OpenAPI Swagger sandbox containing all 18+ modular API environments.

---

## 🌌 Platform Modules

The engine is split into isolated, deeply specialized analytical domains:

### 1. API Mapping (`/api/v1/*`)
- **`/astronomy`**: Core spatial coordinates, ecliptic math, heliacal phenomena.
- **`/charts`**: Geocentric, Topocentric, Heliocentric, and Vedic D9 chart modeling.
- **`/aspects` & `/transits`**: Orbs boundaries, Ptolemaic/Kepler scanning, sweeping exact time-hits for cross-domain alignments.
- **`/financial`**: Hardened wrappers tracking eclipses, macro-ingresses, and deep retrograde blocks (structurally sandboxed).
- **`/signals` & `/quant`**: Phase velocity tracking, event clustering, intense density calculations.
- **`/research`**: Capable of dumping 5-year longitudinal ephemeris structures in pure CSV or mass JSON arrays.
- **`/vedic`**: Support for Vimshottari Dashas (down to Level 3 Pratyantardasha recursively), Ashtakavarga matrices, and Shadbala structural layouts.
- **`/alerts`**: Supports persistent SQLModel database logic pushed into `FastAPI BackgroundTasks` to asynchronously trace thousands of planetary bounds constantly.

### 2. High-Performance Core Layer
At the absolute center of AstroSDK sits the `app.core.ephemeris.Ephemeris` singleton. To prevent PySwissEph's synchronous C-library locks from blocking concurrent asynchronous traffic, all primary boundary points incorporate robust `lru_cache` mechanics.

---

## 🧪 Testing & Reliability

AstroSDK maintains an impeccable zero-tolerance failure standard. The regression test suite guarantees mathematically precise outputs enforcing the deterministic rule.

```bash
pytest tests/ -v
```

---

## 🔒 Configuration Echoing

The backend is structurally stateless. Rather than persisting User Config into SQLite and accidentally breaking the Determinism guarantees, the API supports a `POST /api/v1/astro/settings` schema. This accepts a client's ruleset (Ayanamsas, House definitions), validates it recursively, enforces boundaries, and echoes the schema back for the client to attach to subsequent analytical API calls.

## 🔗 Deep Swiss Ephemeris Backing

AstroSDK supports **47 ayanamsa systems** natively ported from Swiss Ephemeris, spanning:
- `LAHIRI` (Base Standard)
- `FAGAN_BRADLEY`
- `KRISHNAMURTI` 
- Babylon, Galactic Centroids, J2000, and standard Equatorial mapping.

All internal coordinate parsing adheres tightly to true geometric principles (Delta-T validation, Julian Day conversion vectors). 

---

**Built with precision. Scaled for Enterprise Architecture.**
