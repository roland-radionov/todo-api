from pydantic_settings import BaseSettings
from pydantic import BaseModel

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private-key.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public-key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///todo.db"
    debug: bool = True
    jwt_auth: AuthJWT = AuthJWT()


settings = Settings()
