from enum import StrEnum

from pydantic import BaseModel, Field


class FeatureMaturity(StrEnum):
    EXPERIMENTAL = "experimental"
    BETA = "beta"
    PRODUCTION = "production"


class FeatureContext(BaseModel):
    """Execution metadata that describes feature readiness and behavior."""

    capability: str = Field(..., description="Canonical capability identifier.")
    maturity: FeatureMaturity = Field(
        default=FeatureMaturity.EXPERIMENTAL,
        description="Current feature maturity level.",
    )
    notes: str | None = Field(
        default=None,
        description="Optional implementation notes for operators and API metadata.",
    )
