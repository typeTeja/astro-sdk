from dataclasses import dataclass

from ..contexts.feature import FeatureMaturity


@dataclass(frozen=True)
class CapabilityRegistration:
    capability: str
    maturity: FeatureMaturity
    owner: str
    summary: str


CAPABILITY_REGISTRY: dict[str, CapabilityRegistration] = {
    "core.generic": CapabilityRegistration(
        capability="core.generic",
        maturity=FeatureMaturity.EXPERIMENTAL,
        owner="core",
        summary="Base capability used by shared 2.0 scaffold components.",
    ),
}
