from app.contexts import CalculationContext


class MundaneStationService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
