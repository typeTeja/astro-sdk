# AstroSDK Service Deployment Commands

Before launching, always ensure your Python virtual environment is active and dependencies are loaded.

```bash
# Activate environment
source .venv/bin/activate
```

## Running the Architecture Globally (Development)

For local development across all 18+ modular endpoints:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Available at: `http://localhost:8000`
- Swagger Sandbox: `http://localhost:8000/docs`

## Background Task Scanning Architecture

If you intend to use the intensive automated background alerting suite (`/api/v1/alerts/scan?background=true`), ensure your deployment server does not spin down async threads unexpectedly, or migrate to a Celery wrapper.

## Running Tests
Validating the deterministic bounds across the entire system:
```bash
pytest tests/ -v
```
