from dataclasses import dataclass
from datetime import datetime

from app.core.constants import Planet
from app.domain.common.metadata import DomainMetadata


@dataclass(frozen=True)
class MundaneIngress:
    planet: Planet
    from_sign: str
    to_sign: str
    time: datetime
    metadata: DomainMetadata
