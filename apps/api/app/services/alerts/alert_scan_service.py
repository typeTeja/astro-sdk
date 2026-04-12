from typing import Any

from sqlmodel import Session, select

from app.contexts.calculation import CalculationContext
from app.core.ephemeris import Ephemeris
from app.models.alerts import AlertRule


class AlertScanService:
    """AstroSDK 2.0 service for scanning and executing alert rules."""

    def __init__(self, context: CalculationContext, session: Session, ephemeris: Ephemeris) -> None:
        self.context = context
        self.session = session
        self.ephemeris = ephemeris

    def scan_active_rules(self, window_days: float) -> list[Any]:
        """
        Scan all active rules in the database and detect triggers.
        Returns a list of match objects for the API to map.
        """
        statement = select(AlertRule).where(AlertRule.is_active)
        # Scan logic placeholder: execute summary check
        _ = self.session.exec(statement).all()

        results: list[Any] = []
        return results
