from pydantic import BaseModel, Field


class ObserverContext(BaseModel):
    """Observer location used for topocentric and horizon-sensitive work."""

    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    altitude: float = Field(default=0.0)
