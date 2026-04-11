from ..contexts import CalculationContext


class AstroSDKClient:
    """Minimal entry point for future first-party AstroSDK SDK surfaces."""

    def __init__(self, context: CalculationContext | None = None) -> None:
        self.context = context or CalculationContext()
