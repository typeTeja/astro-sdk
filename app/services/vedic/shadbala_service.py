from app.contexts import CalculationContext


class VedicShadbalaService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
