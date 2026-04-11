from ...contexts import CalculationContext


class MundaneIngressService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
