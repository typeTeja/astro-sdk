from typing import Optional

class AstroError(Exception):
    """Base exception for all AstroSDK errors."""
    pass

class EphemerisError(AstroError):
    """Raised when the Ephemeris provider encounters an error."""
    def __init__(self, message: str, code: Optional[int] = None):
        super().__init__(f"Ephemeris Error: {message} (Code: {code})")
        self.code = code

class InvalidTimeError(AstroError):
    """Raised when time input is invalid or ambiguous."""
    pass

class ConfigurationError(AstroError):
    """Raised when SDK configuration is invalid."""
    pass

class EphemerisStateError(AstroError):
    """Raised when there is a conflict in the internal state."""
    pass

class InvalidTimeStandardError(AstroError):
    """Raised when a time standard (like ET) is passed to a UT-only API."""
    pass

class UnsupportedPlanetError(AstroError):
    """Raised when a fictional or unsupported body is requested."""
    pass

class SearchRangeTooLargeError(AstroError):
    """Raised when a search operation exceeds performance guardrails."""
    pass
