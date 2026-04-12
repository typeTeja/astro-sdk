import hashlib
import json
from typing import Any


def calculation_fingerprint(payload: dict[str, Any]) -> str:
    """Return a deterministic fingerprint for calculation metadata."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
