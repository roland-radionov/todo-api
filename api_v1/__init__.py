from fastapi import APIRouter

from .tasks import tasks_router
from .users import users_router
from .jwt_auth import jwt_auth_router

router = APIRouter(prefix="/api/v1")
router.include_router(tasks_router)
router.include_router(users_router)
router.include_router(jwt_auth_router)


__all__ = ["router"]
