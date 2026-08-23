from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path | None = None
    public_key_path: Path | None = None
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

    def get_private_key(self) -> str:
        path = (
            self.private_key_path
            if self.private_key_path
            else BASE_DIR / "certs" / "private-key.pem"
        )
        if not path.exists():
            raise FileNotFoundError(f"Private key not found: {path}")

        return path.read_text()

    def get_public_key(self) -> str:
        path = (
            self.public_key_path
            if self.public_key_path
            else BASE_DIR / "certs" / "public-key.pem"
        )
        if not path.exists():
            raise FileNotFoundError(f"Public key not found: {path}")

        return path.read_text()


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///todo.db"
    debug: bool = True
    jwt_auth: AuthJWT = AuthJWT()


settings = Settings()
