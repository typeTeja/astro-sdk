from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from ...core.database import get_session
from ...core.ephemeris import Ephemeris
from ...models.alerts import AlertRule
from ...schemas.alerts import (
    AlertRuleCreate,
    AlertRuleData,
    AlertRuleListResponse,
    AlertRuleResponse,
    AlertScanResponse,
    AlertScanResult,
)
from ...services.scanner_service import ScannerService
from .meta import get_meta

router = APIRouter()
ephemeris = Ephemeris()


@router.post("/rules", response_model=AlertRuleResponse, summary="Create a new alert rule")
async def create_rule(
    rule_in: AlertRuleCreate, session: Annotated[Session, Depends(get_session)]
) -> AlertRuleResponse:
    """
    Define a new planetary trigger (Ingress, Station, or Aspect).
    """
    # Create persistent rule from schema
    rule = AlertRule(
        name=rule_in.name,
        planet=rule_in.planet,
        secondary_planet=rule_in.secondary_planet,
        event_type=rule_in.event_type,
        target_value=rule_in.target_value,
        webhook_url=rule_in.webhook_url,
        is_active=rule_in.is_active,
    )

    session.add(rule)
    session.commit()
    session.refresh(rule)

    # Map model to schema data
    data = AlertRuleData(
        id=rule.id,
        name=rule.name,
        planet=rule.planet.name,
        secondary_planet=rule.secondary_planet.name if rule.secondary_planet else None,
        event_type=rule.event_type,
        target_value=rule.target_value,
        is_active=rule.is_active,
    )

    return AlertRuleResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)


@router.get("/rules", response_model=AlertRuleListResponse, summary="List all alert rules")
async def get_rules(session: Annotated[Session, Depends(get_session)]) -> AlertRuleListResponse:
    """
    Retrieve all active/inactive alert rules from persistence.
    """
    rules = session.exec(select(AlertRule)).all()

    # Map models to schema data
    data = [
        AlertRuleData(
            id=r.id,
            name=r.name,
            planet=r.planet.name,
            secondary_planet=r.secondary_planet.name if r.secondary_planet else None,
            event_type=r.event_type,
            target_value=r.target_value,
            is_active=r.is_active,
        )
        for r in rules
    ]

    return AlertRuleListResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=data)


from fastapi import BackgroundTasks

@router.post("/scan", summary="Run manual scan for triggers")
async def scan_alerts(
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
    window_days: float = Query(1.0, ge=0.1, le=365.0),
    background: bool = Query(False, description="Run scan silently in background to avoid blocking"),
) -> dict | AlertScanResponse:
    """
    Trigger a scan of all active rules within a given look-back window.
    """
    if background:
        # Create a fresh isolated session for the background thread,
        # session is attached to current request state. To be truly safe with SQLAlchemy/SQLModel:
        # It's better to instantiate a new session inside the background task if it takes too long.
        # But for this simple implementation:
        def bg_scan(w_days: float):
            from ...core.database import SessionLocal
            with SessionLocal() as bg_session:
                scanner = ScannerService(bg_session, ephemeris)
                scanner.scan_active_rules(w_days)
                
        background_tasks.add_task(bg_scan, window_days)
        return {"meta": get_meta(is_sidereal=False, sidereal_mode=None).model_dump(), "data": {"status": "Accepted. Scanning running in background."}}

    scanner = ScannerService(session, ephemeris)
    results = scanner.scan_active_rules(window_days)

    # Map raw scanner output to AlertScanResult
    mapped = []
    for r in results:
        mapped.append(
            AlertScanResult(
                rule_id=r.get("rule_id", 0),
                name=r.get("name", "Unknown"),
                event=r.get("event", "Triggered"),
                time=r.get("time"),
                details=r.get("details", ""),
            )
        )

    return AlertScanResponse(meta=get_meta(is_sidereal=False, sidereal_mode=None), data=mapped)

@router.delete("/{rule_id}", summary="Delete an alert rule")
async def delete_rule(
    rule_id: int, session: Annotated[Session, Depends(get_session)]
) -> dict[str, str]:
    """
    Remove an alert rule permanently from the database.
    """
    rule = session.get(AlertRule, rule_id)
    if not rule:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Rule not found")
        
    session.delete(rule)
    session.commit()
    return {"status": "success", "message": f"Rule {rule_id} deleted."}
