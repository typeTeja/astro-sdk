from dataclasses import dataclass
from datetime import datetime

from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class PanchangaData:
    """
    Domain model for the five elements of Vedic time.
    """
    tithi: str
    vara: str
    nakshatra: str
    yoga: str
    karana: str
    sunrise: datetime
    sunset: datetime
    metadata: DomainMetadata
