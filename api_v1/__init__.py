from fastapi import APIRouter

from .auth import auth_router
from .tasks import tasks_router
from .users import users_router

router = APIRouter(prefix="/api_v1")
router.include_router(tasks_router)
router.include_router(users_router)
router.include_router(auth_router)


__all__ = ["router"]
