from functools import lru_cache

from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings


@lru_cache
class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    WEBAPP_URL: str
    DEBUG: bool
    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = "./.env"

    @property
    def DATABASE_URI(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=self.DB_NAME,
        )


config = Config()
