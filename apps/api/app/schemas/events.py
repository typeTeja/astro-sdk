from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseAstroResponse


class IngressSchema(BaseModel):
    """
    Planetary sign boundary crossing.
    """

    planet: str
    time: datetime
    from_sign: str
    to_sign: str


class IngressResponse(BaseAstroResponse[list[IngressSchema]]):
    pass


class RetrogradeSchema(BaseModel):
    """
    Planetary station event.
    """

    planet: str
    time: datetime
    station_type: str = Field(..., description="RETROGRADE or DIRECT")


class RetrogradeResponse(BaseAstroResponse[list[RetrogradeSchema]]):
    pass


class AstroEventSchema(BaseModel):
    """
    Any significant astronomical event (Aspect, Ingress, Station).
    """

    planet: str
    event_type: str
    time: datetime
    details: str
    is_major: bool = True


class GlobalEventsResponse(BaseAstroResponse[list[AstroEventSchema]]):
    pass
