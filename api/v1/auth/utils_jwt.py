from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt_auth.get_private_key(),
    algorithm: str = settings.jwt_auth.algorithm,
    expires_delta: timedelta | None = None,
):
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.jwt_auth.access_token_expire_minutes
        )
    to_encode.update({"exp": expire, "iat": datetime.now(UTC)})
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt_auth.get_public_key(),
    algorithm: str = settings.jwt_auth.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    bytes = password.encode()
    return bcrypt.hashpw(bytes, salt).decode("utf-8")


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
