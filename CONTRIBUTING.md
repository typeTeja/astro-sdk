# Contributing to AstroSDK

Thank you for your interest in contributing to AstroSDK! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- Check the existing issues to avoid duplicates
- Verify the bug exists in the latest version

When creating a bug report, include:
- Python version and OS
- pyswisseph version
- Minimal code to reproduce the issue
- Expected vs actual behavior
- Full error traceback

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Check existing issues/PRs for similar suggestions
- Clearly describe the use case
- Explain why this enhancement would be useful
- Consider if it aligns with the project's core principles (determinism, correctness, auditability)

### Pull Requests

1. **Fork the repository** and create a branch from `main`
2. **Follow the coding standards** (see below)
3. **Add tests** for any new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** (`pytest tests/ -v`)
6. **Run type checking** (`mypy src/astrosdk --strict`)
7. **Run linting** (`ruff check src/astrosdk`)
8. **Submit the PR** with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/astrosdk.git
cd astrosdk

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/astrosdk --cov-report=term-missing
```

## Coding Standards

### Core Principles

AstroSDK prioritizes:
1. **Correctness over Speed** - Never compromise astronomical precision
2. **Determinism over Convenience** - Same input must produce identical output
3. **Explicitness over Brevity** - No hidden defaults or assumptions
4. **Auditability over Abstraction** - Every calculation must be traceable

### Code Style

- **Type Hints**: All functions must have complete type hints
- **Immutability**: Use `@dataclass(frozen=True)` for domain models
- **No Side Effects**: Service functions must be pure (no I/O, no logging)
- **Thread Safety**: All Swiss Ephemeris calls must be protected by locks
- **Error Handling**: Use structured exceptions, never raw `Exception`

### Formatting

```bash
# Check formatting
ruff format --check src/astrosdk tests/

# Auto-format
ruff format src/astrosdk tests/
```

### Type Checking

```bash
# Run mypy in strict mode
mypy src/astrosdk --strict
```

All code must pass strict type checking with no errors.

### Testing

- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test service coordination
- **Regression Tests**: Test known astronomical events with expected values
- **Edge Cases**: Test boundary conditions and error handling

Test naming convention: `test_<functionality>_<scenario>`

```python
def test_retrograde_detection_mercury():
    """Test retrograde detection for Mercury at known retrograde period."""
    # ...
```

## Architecture Guidelines

### Layer Separation

```
core/       - Swiss Ephemeris wrapper, time handling, constants
domain/     - Immutable data models (no business logic)
services/   - Business logic (pure functions, no side effects)
engine/     - High-level orchestration
```

**Rules:**
- Core layer: Only Swiss Ephemeris interaction
- Domain layer: Only data structures and computed properties
- Services layer: No I/O, no printing, no logging
- Engine layer: Coordinate multiple services

### What NOT to Add

AstroSDK is infrastructure, not an application. Do NOT add:
- ❌ HTTP APIs or web frameworks
- ❌ Database integrations
- ❌ Machine learning or AI
- ❌ Interpretation or prediction logic
- ❌ Financial advice or signals
- ❌ UI components

## Documentation

### Docstrings

Use NumPy-style docstrings:

```python
def calculate_planet(self, jd: float, planet: Planet) -> Dict[str, float]:
    """
    Calculate planet position at given Julian Day.
    
    Parameters
    ----------
    jd : float
        Julian Day in Universal Time (UT)
    planet : Planet
        Planet enum member
        
    Returns
    -------
    Dict[str, float]
        Dictionary containing longitude, latitude, distance, and speeds
        
    Raises
    ------
    UnsupportedPlanetError
        If planet is not in ALLOWED_PLANETS
    EphemerisError
        If Swiss Ephemeris calculation fails
    """
```

### README Updates

When adding new features, update:
- Quick start examples (if applicable)
- Supported calculations section
- API reference (when available)

## Commit Messages

Follow conventional commits:

```
feat: add support for heliacal phenomena
fix: correct retrograde detection at station points
docs: update README with new examples
test: add edge cases for extreme latitudes
refactor: extract common validation logic
```

## Release Process

1. Update `CHANGELOG.md` with changes
2. Bump version in `pyproject.toml`
3. Run full test suite
4. Create git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
5. Push tag: `git push origin v1.0.0`
6. GitHub Actions will handle the rest

## Questions?

- Open a GitHub Discussion for general questions
- Open an issue for bug reports or feature requests
- Email security@yourdomain.com for security vulnerabilities

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make AstroSDK better! 🌟
