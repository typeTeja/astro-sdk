from app.contexts import CalculationContext


class ResearchExportService:
    def __init__(self, context: CalculationContext) -> None:
        self.context = context
