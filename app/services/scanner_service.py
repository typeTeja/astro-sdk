from datetime import UTC, datetime
from typing import Any

from sqlmodel import Session, select

from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..models.alerts import AlertRule
from .crossing_service import CrossingService


class ScannerService:
    """
    Engine for evaluating persistent alert rules against the astronomical timeline.
    """

    def __init__(self, session: Session, ephemeris: Ephemeris):
        self.session = session
        self.eph = ephemeris
        self.crossing_service = CrossingService(ephemeris)

    def scan_active_rules(self, window_days: float = 1.0) -> list[dict[str, Any]]:
        """
        Scan all active rules for triggers in the last N days.
        """
        statement = select(AlertRule).where(AlertRule.is_active)
        rules = self.session.exec(statement).all()

        # Window: [Now - window_days, Now]
        end_time = Time(datetime.now(UTC))
        start_time = Time.from_julian_day(end_time.julian_day - window_days)

        hits = []
        for rule in rules:
            hit_result = None

            if rule.event_type == "INGRESS":
                ingresses = self.crossing_service.find_ingresses(rule.planet, start_time, end_time)
                if ingresses:
                    hit_result = {
                        "rule_id": rule.id,
                        "name": rule.name,
                        "event": "INGRESS",
                        "time": ingresses[0].time,
                        "details": f"Entered Sign {ingresses[0].sign_id}",
                    }

            elif rule.event_type == "STATION":
                stations = self.crossing_service.find_stations(rule.planet, start_time, end_time)
                if stations:
                    hit_result = {
                        "rule_id": rule.id,
                        "name": rule.name,
                        "event": "STATION",
                        "time": stations[0].time,
                        "details": "Turned "
                        + ("Retrograde" if stations[0].is_retrograde else "Direct"),
                    }

            elif rule.event_type == "ASPECT":
                # Ensure secondary planet and target angle exist
                if rule.secondary_planet is not None and rule.target_value is not None:
                    aspects = self.crossing_service.find_aspects(
                        rule.planet, rule.secondary_planet, rule.target_value, start_time, end_time
                    )
                    if aspects:
                        hit_result = {
                            "rule_id": rule.id,
                            "name": rule.name,
                            "event": "ASPECT",
                            "time": aspects[0].time,
                            "details": f"Hit {rule.target_value}deg aspect between {rule.planet.name} and {rule.secondary_planet.name}",
                        }

            if hit_result:
                hits.append(hit_result)
                # Update last_triggered
                rule.last_triggered = hit_result["time"]
                self.session.add(rule)

        self.session.commit()
        return hits
