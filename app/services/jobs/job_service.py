import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any, Callable

from sqlmodel import Session, select
from app.models.jobs import Job, JobStatus

logger = logging.getLogger(__name__)


class JobService:
    """
    Service for managing background tasks with persistence and a thread pool.
    """

    # Shared thread pool for all job execution
    _executor = ThreadPoolExecutor(max_workers=4)

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_job(self, task_type: str, payload: dict[str, Any]) -> Job:
        """Create and persist a new job record."""
        job = Job(task_type=task_type, payload=payload, status=JobStatus.PENDING)
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def submit_task(self, job_id: int, task_func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Submit a task for background execution."""
        job = self.session.get(Job, job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found.")

        job.status = JobStatus.RUNNING
        job.updated_at = datetime.now(UTC)
        self.session.add(job)
        self.session.commit()

        # Submit to thread pool
        self._executor.submit(self._run_task_wrapper, job_id, task_func, *args, **kwargs)

    def _run_task_wrapper(self, job_id: int, task_func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Internal wrapper to handle job state updates and error handling."""
        # Use a fresh session for the background thread to avoid thread-safety issues
        from app.core.database import engine
        
        try:
            with Session(engine) as session:
                job = session.get(Job, job_id)
                if not job:
                    return

                try:
                    # Execute the actual task
                    result = task_func(*args, **kwargs)
                    
                    job.status = JobStatus.COMPLETED
                    job.result_url = str(result) if result else None
                    job.completed_at = datetime.now(UTC)
                except Exception as e:
                    logger.exception(f"Job {job_id} failed: {e}")
                    job.status = JobStatus.FAILED
                    job.error_message = str(e)
                
                job.updated_at = datetime.now(UTC)
                session.add(job)
                session.commit()
        except Exception as e:
            logger.error(f"Critical error in job wrapper for job {job_id}: {e}")

    def get_job_status(self, job_id: int) -> Job | None:
        """Retrieve the current state of a job."""
        return self.session.get(Job, job_id)

    def get_recent_jobs(self, limit: int = 20) -> list[Job]:
        """List recently created jobs."""
        statement = select(Job).order_by(Job.created_at.desc()).limit(limit)
        return list(self.session.exec(statement).all())
