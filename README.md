# AstroSDK 2.0
**Enterprise-Scale Deterministic Astrology API Platform**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AstroSDK 2.0 is a complete graduation of the platform into a high-concurrency, stateless microservice architecture. It provides deterministic astronomical calculations powered by the **Swiss Ephemeris** for research, financial analysis, and enterprise-grade data science.

## 🌌 2.0 Architecture
The 2.0 era introduces a strictly namespaced service layer and a context-driven calculation engine.

### Core Modules (`/api/v2/*`)
- **`/astronomy`**: High-precision coordinates, lunar cycles, and horizon events.
- **`/western`**: Comprehensive natal, transit, progression, and synastry modeling.
- **`/vedic`**: Native support for Dashas, Panchanga, Ashtakavarga, and Shadbala.
- **`/mundane`**: Global event scanning, ingresses, and planetary stations.
- **`/research`**: Quantitative signals, financial correlations, and batch data export.

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### Launch Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Interactive documentation is available at `http://localhost:8000/docs`.

## 🧪 Testing
AstroSDK 2.0 maintains a 100% deterministic standard.
```bash
python3 -m pytest tests/ -v
```

---
**Built with precision. Scaled for Enterprise Architecture.**
