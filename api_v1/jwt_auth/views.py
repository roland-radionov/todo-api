from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .schemas import Token
from core.models import User
from core.database import get_db
from auth import utils_jwt
from typing import Annotated
import jwt

router = APIRouter(prefix="/auth", tags=["JWT Real Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = utils_jwt.decode_jwt(token)
        if not payload:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    username = payload.get("username")
    if not username:
        raise credentials_exception

    result = await session.execute(select(User).where(User.username == username))
    user: User = result.scalar()
    if not user:
        raise credentials_exception

    return user


@router.post("/login", response_model=Token)
async def auth_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db),
) -> Token:
    result = await session.execute(
        select(User).where(User.username == form_data.username)
    )
    user: User = result.scalar()

    if not user or not utils_jwt.validate_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    access_jwt_token = utils_jwt.encode_jwt(payload)
    return Token(access_token=access_jwt_token)
