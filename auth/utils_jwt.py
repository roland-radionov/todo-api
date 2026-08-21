import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt_auth.private_key_path.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
    expires_delta: timedelta | None = None,
):
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_auth.access_token_expire_minutes
        )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt_auth.public_key_path.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes = password.encode()
    return bcrypt.hashpw(bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
