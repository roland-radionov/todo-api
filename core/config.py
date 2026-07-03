from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///todo.db"

    debug: bool = True

settings = Settings()