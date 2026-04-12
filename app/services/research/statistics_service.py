from app.contexts import CalculationContext


class ResearchStatisticsService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
