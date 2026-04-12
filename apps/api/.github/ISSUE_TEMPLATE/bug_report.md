---
name: Bug Report
about: Report a bug or unexpected behavior in AstroSDK 2.0
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
A clear and concise description of what the bug is.

## To Reproduce
Steps to reproduce the behavior:
1. Initialize `CalculationContext` with '...'
2. Call namespaced service '...'
3. Observe unexpected output or error

## Minimal Code Example (2.0 Patterns)
```python
from app.contexts.factories import create_default_context
from app.services.western.chart_service import WesternChartService
from app.core.time import Time
from datetime import datetime, UTC

# 1. Setup Context
context = create_default_context()

# 2. Setup Service
service = WesternChartService(context)

# 3. Trigger Bug
# ...
```

## Environment
- **OS:** [e.g., Ubuntu 24.04, macOS 14]
- **Python Version:** [e.g., 3.12.2]
- **AstroSDK Version:** 2.0.0
- **pyswisseph Version:** [e.g., 2.10.3.2]

## Additional Context
Add any other context about the problem here.

## Checklist
- [ ] I have searched existing issues to avoid duplicates
- [ ] I have tested with the latest 2.0 version
- [ ] I have included a minimal reproducible 2.0 example
- [ ] I have included the full error traceback
