from app.contexts import (
    CalculationContext,
    CoordinateContext,
    CoordinateSystem,
    FeatureContext,
    FeatureMaturity,
    HouseContext,
    ObserverContext,
    TimeContext,
    ZodiacContext,
    ZodiacType,
)
from app.core.fingerprint import calculation_fingerprint
from app.core.registry import CAPABILITY_REGISTRY, CapabilityRegistration
from app.sdk import AstroSDKClient
from app.services.western import WesternChartService


def test_calculation_context_defaults_are_constructible() -> None:
    context = CalculationContext()

    assert context.zodiac.zodiac == ZodiacType.SIDEREAL
    assert context.coordinate.system == CoordinateSystem.GEOCENTRIC
    assert context.observer is None
    assert context.feature.capability == "core.generic"


def test_context_components_can_be_composed_explicitly() -> None:
    context = CalculationContext(
        zodiac=ZodiacContext(zodiac=ZodiacType.TROPICAL, sidereal_mode=None),
        coordinate=CoordinateContext(system=CoordinateSystem.TOPOCENTRIC),
        observer=ObserverContext(latitude=12.97, longitude=77.59, altitude=920.0),
        house=HouseContext(),
        time=TimeContext(tolerance_seconds=0.5, max_search_days=365.0),
        feature=FeatureContext(
            capability="western.chart",
            maturity=FeatureMaturity.BETA,
        ),
    )

    assert context.zodiac.is_sidereal is False
    assert context.coordinate.is_topocentric is True
    assert context.observer is not None
    assert context.feature.maturity == FeatureMaturity.BETA


def test_calculation_fingerprint_is_deterministic() -> None:
    payload = {"capability": "western.chart", "mode": "sidereal", "version": 2}

    first = calculation_fingerprint(payload)
    second = calculation_fingerprint(payload)

    assert first == second
    assert len(first) == 64


def test_calculation_context_fingerprint_payload_is_stable() -> None:
    context = CalculationContext()

    payload = context.fingerprint_payload()

    assert payload["feature"]["capability"] == "core.generic"
    assert payload["coordinate"]["system"] == "geocentric"


def test_capability_registry_has_valid_registration_shape() -> None:
    registration = CAPABILITY_REGISTRY["core.generic"]

    assert isinstance(registration, CapabilityRegistration)
    assert registration.capability == "core.generic"
    assert registration.maturity == FeatureMaturity.EXPERIMENTAL


def test_sdk_and_grouped_service_scaffold_imports_are_usable() -> None:
    client = AstroSDKClient()
    service = WesternChartService(client.context)

    assert isinstance(client.context, CalculationContext)
    assert service.context is client.context
