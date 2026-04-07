from sqlmodel import Session, select

from ..core.ephemeris import Ephemeris
from ..models.alerts import AlertRule


class AlertService:
    """
    Orchestration service for managing planetary alerts.
    """

    def __init__(self, session: Session, ephemeris: Ephemeris) -> None:
        self.session = session
        self.eph = ephemeris

    def create_rule(self, rule: AlertRule) -> AlertRule:
        """Persist a new alert rule."""
        self.session.add(rule)
        self.session.commit()
        self.session.refresh(rule)
        return rule

    def get_all_active_rules(self) -> list[AlertRule]:
        """Retrieve all rules where is_active is True."""
        statement = select(AlertRule).where(AlertRule.is_active)
        return list(self.session.exec(statement).all())

    def delete_rule(self, rule_id: int) -> None:
        """Remove a rule from persistence."""
        rule = self.session.get(AlertRule, rule_id)
        if rule:
            self.session.delete(rule)
            self.session.commit()
