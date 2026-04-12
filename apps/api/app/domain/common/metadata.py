from dataclasses import dataclass


@dataclass(frozen=True)
class DomainMetadata:
    """Shared metadata for AstroSDK 2.0 domain objects."""

    capability: str
    maturity: str
    fingerprint: str | None = None
