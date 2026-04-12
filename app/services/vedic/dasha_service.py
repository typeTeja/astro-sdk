from app.contexts import CalculationContext


class VedicDashaService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
