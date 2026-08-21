from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from .schemas import UserResponse, UserCreate
from .crud import get_user_by_id, create_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user_by_id_view(
    user_id: int, session: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await get_user_by_id(session=session, id=user_id)


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register_view(
    user_in: UserCreate, session: AsyncSession = Depends(get_db)
) -> UserResponse:
    user = await create_user(session=session, user_in=user_in)
    return user
