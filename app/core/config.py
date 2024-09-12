from typing import List
from pydantic import AnyHttpUrl, MySQLDsn
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    EXPIRE_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "LINACCONTROL"
    MYSQL_SERVER: str = config("MYSQL_SERVER", cast=str)
    MYSQL_PORT: int = config("MYSQL_PORT", cast=int)
    MYSQL_USER: str = config("MYSQL_USER", cast=str)
    MYSQL_PASSWORD: str = config("MYSQL_PASSWORD", cast=str)
    MYSQL_DB: str = config("MYSQL_DB", cast=str)

    @property
    def DATABASE_URI(self):
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    class Config:
        case_sensitive = True

settings = Settings()
