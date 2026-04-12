from app.contexts import CalculationContext


class VedicVargaService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
