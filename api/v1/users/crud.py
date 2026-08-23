from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import utils_jwt
from core.models import User

from .schemas import UserCreate


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user_attrs = user_in.model_dump()
    username = user_attrs["username"]
    email = user_attrs["email"]
    result = await session.execute(
        select(User).where((User.username == username) | (User.email == email))
    )
    user = result.scalar()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registred"
        )

    user_attrs["hashed_password"] = utils_jwt.hash_password(user_attrs["password"])
    del user_attrs["password"]
    user = User(**user_attrs)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    return await session.get(User, id)
