from datetime import datetime

from pydantic import BaseModel

from .base import BaseAstroResponse


class SynodicPhaseSchema(BaseModel):
    """
    Relative phase between two planets (0-360).
    """

    p1: str
    p2: str
    phase: float
    is_applying: bool


class SynodicPhaseResponse(BaseAstroResponse[SynodicPhaseSchema]):
    pass


class SynodicEventSchema(BaseModel):
    """
    Exact conjunction/opposition event.
    """

    p1: str
    p2: str
    time: datetime
    angle: float


class SynodicEventResponse(BaseAstroResponse[SynodicEventSchema]):
    pass


class AstroIndicatorSchema(BaseModel):
    """
    Quantitative metrics for a single point in time.
    """

    time: datetime
    indicators: dict[str, float]
    price_mapping: float | None = None


class AstroIndicatorResponse(BaseAstroResponse[AstroIndicatorSchema]):
    pass


class AstroIndicatorScanResponse(BaseAstroResponse[list[AstroIndicatorSchema]]):
    pass


class QuantScanRequest(BaseModel):
    """
    Request for generating time-series data.
    """

    start_time: str
    end_time: str
    interval_minutes: int = 60
    planets: list[str] | None = None
