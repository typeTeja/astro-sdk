from ...contexts import CalculationContext


class ResearchScanService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
