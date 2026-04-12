from typing import Any

from ...contexts import CalculationContext, FeatureMaturity
from ...core.fingerprint import calculation_fingerprint


def capability_metadata(capability: str, maturity: FeatureMaturity) -> dict[str, str]:
    return {"capability": capability, "maturity": maturity.value}


def calculation_metadata(
    context: CalculationContext,
    *,
    primary_inputs: dict[str, Any],
) -> dict[str, str]:
    payload = {
        "context": context.fingerprint_payload(),
        "inputs": primary_inputs,
    }
    return {
        "capability": context.feature.capability,
        "feature_maturity": context.feature.maturity.value,
        "calculation_fingerprint": calculation_fingerprint(payload),
    }
