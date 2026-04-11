from fastapi import APIRouter
from .astronomy.positions import router as astronomy_router
from .western.charts import router as western_router
from .vedic.panchang import router as vedic_router
from .research.jobs import router as research_router
from .alerts.rules import router as alert_router

router = APIRouter()

router.include_router(astronomy_router, prefix="/astronomy", tags=["Astronomy"])
router.include_router(western_router, prefix="/western", tags=["Western"])
router.include_router(vedic_router, prefix="/vedic", tags=["Vedic"])
router.include_router(research_router, prefix="/research", tags=["Research"])
router.include_router(alert_router, prefix="/alerts", tags=["Alerts"])
