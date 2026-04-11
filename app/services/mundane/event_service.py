from ...contexts import CalculationContext


class MundaneEventService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
