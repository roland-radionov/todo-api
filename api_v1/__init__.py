from .tasks import tasks_router
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")
router.include_router(tasks_router)


__all__ = ["router"]
