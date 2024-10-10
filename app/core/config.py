from typing import List
from pydantic import AnyHttpUrl, MySQLDsn
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EXPIRE_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REFRESH_EXPIRE_TOKEN_DAYS: int = 2
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "LINACCONTROL"
    DATABASE_SERVER: str = config("DATABASE_SERVER", cast=str)
    DATABASE_PORT: int = config("DATABASE_PORT", cast=int)
    DATABASE_USER: str = config("DATABASE_USER", cast=str)
    DATABASE_PASSWORD: str = config("DATABASE_PASSWORD", cast=str)
    DATABASE_NAME: str = config("DATABASE_NAME", cast=str)
    ADMIN_FIRST_NAME: str = config("ADMIN_FIRST_NAME", cast=str)
    ADMIN_LAST_NAME: str = config("ADMIN_LAST_NAME", cast=str)
    ADMIN_USERNAME: str = config("ADMIN_USERNAME", cast=str)
    ADMIN_PASSWORD: str = config("ADMIN_PASSWORD", cast=str)

    @property
    def DATABASE_URI(self):
        return f"mysql+asyncmy://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_SERVER}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    class Config:
        case_sensitive = True


settings = Settings()
