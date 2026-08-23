from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

from .crud import get_user_by_id
from .schemas import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user_by_id_view(
    user_id: int, session: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await get_user_by_id(session=session, id=user_id)
