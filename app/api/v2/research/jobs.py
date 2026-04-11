from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from ....core.database import get_session
from ....models.jobs import Job
from ....services.jobs.job_service import JobService
from ..common import get_calculation_context

router = APIRouter()


@router.post("/export", summary="[V2] Submit background export job")
async def submit_export_job(
    task_type: str = Query("EXPORT"),
    payload: dict = {},
    session: Session = Depends(get_session)
) -> dict:
    """
    Submit a long-running research export to the 2.0 job engine.
    """
    service = JobService(session)
    job = service.create_job(task_type, payload)
    
    # In a real v2, we would trigger the specific service task here
    # For now we track the submission
    return {
        "job_id": job.id,
        "status": job.status,
        "message": "Job submitted and tracked in persistence."
    }


@router.get("/status/{job_id}", summary="[V2] Check job status")
async def get_job_status(
    job_id: int,
    session: Session = Depends(get_session)
) -> Job:
    """
    Poll the status of a background research job.
    """
    service = JobService(session)
    job = service.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
