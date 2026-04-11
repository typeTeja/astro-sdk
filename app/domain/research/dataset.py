from dataclasses import dataclass

from ..common.metadata import DomainMetadata


@dataclass(frozen=True)
class DatasetExport:
    export_name: str
    format: str
    metadata: DomainMetadata
