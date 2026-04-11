from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from ....core.database import get_session
from ....models.alerts import AlertRule
from ....services.alerts.alert_rule_service import AlertRuleService

router = APIRouter()


@router.post("/rules", summary="[V2] Create alert rule")
async def create_alert_rule(
    rule: AlertRule,
    session: Session = Depends(get_session)
) -> AlertRule:
    """
    Store a new high-precision planetary alert rule.
    """
    service = AlertRuleService(session)
    return service.create_rule(rule)


@router.get("/rules", summary="[V2] List all active rules")
async def list_active_rules(
    session: Session = Depends(get_session)
) -> list[AlertRule]:
    """
    Retrieve all monitoring rules with active status.
    """
    service = AlertRuleService(session)
    return service.get_active_rules()


@router.delete("/rules/{rule_id}", summary="[V2] Delete alert rule")
async def delete_alert_rule(
    rule_id: int,
    session: Session = Depends(get_session)
) -> dict:
    """
    Remove an alert rule from the monitoring engine.
    """
    service = AlertRuleService(session)
    service.delete_rule(rule_id)
    return {"status": "DELETED", "id": rule_id}
