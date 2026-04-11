from dataclasses import dataclass

from ...core.constants import Planet
from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class PadaPosition:
    pada: int
    metadata: DomainMetadata


@dataclass(frozen=True)
class NakshatraPosition:
    planet: Planet
    nakshatra: str
    pada: PadaPosition
    metadata: DomainMetadata
