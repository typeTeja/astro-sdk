from dataclasses import dataclass

from app.contexts.feature import FeatureMaturity


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
    "astronomy.positions": CapabilityRegistration(
        capability="astronomy.positions",
        maturity=FeatureMaturity.PRODUCTION,
        owner="core",
        summary="Planetary position and horizontal coordinate calculations.",
    ),
    "western.chart": CapabilityRegistration(
        capability="western.chart",
        maturity=FeatureMaturity.PRODUCTION,
        owner="western",
        summary="Western natal chart generation including planets and houses.",
    ),
    "western.aspects": CapabilityRegistration(
        capability="western.aspects",
        maturity=FeatureMaturity.PRODUCTION,
        owner="western",
        summary="Major, minor, and Kepler aspect calculation between planetary positions.",
    ),
    "vedic.panchanga": CapabilityRegistration(
        capability="vedic.panchanga",
        maturity=FeatureMaturity.PRODUCTION,
        owner="vedic",
        summary="High-precision calculation of the five elements of Vedic time.",
    ),
    "core.ephemeris_isolation": CapabilityRegistration(
        capability="core.ephemeris_isolation",
        maturity=FeatureMaturity.PRODUCTION,
        owner="core",
        summary="Isolation of Swiss Ephemeris global state using EphemerisContext.",
    ),
}
