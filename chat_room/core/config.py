import secrets
from typing import List, Union
from decouple import config
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Chat Room"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    CORS_ORIGINS: Union[str, List[str]] = config("CORS_ORIGINS", default=[])

    LOG_FORMAT: str = config(
        "LOG_FORMAT", default="{time:YYYY-MM-DD HH:mm:ss Z} - {level} - {message}"
    )
    LOG_LEVEL: str = config("LOG_LEVEL", default="DEBUG")

    MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
    MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

    MONGODB_URL: str = f"mongodb://{config('MONGO_INITDB_ROOT_USERNAME')}:{config('MONGO_INITDB_ROOT_PASSWORD')}@{config('MONGO_HOST')}:{config('MONGO_PORT')}/{config('DB_NAME')}?authSource={config('MONGO_AUTHENTICATION_DATABASE')}"
    DB_NAME: str = config("DB_NAME", "")

    JWT_SECRET: str = config("JWT_SECRET", default="")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=15)
    REFRESH_TOKEN_EXPIRE_HOURS: int = config("REFRESH_TOKEN_EXPIRE_HOURS", default=12)

    TIMEZONE: str = config("TIMEZONE", default="Asia/Dhaka")

    @validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("LOG_LEVEL")
    def validate_log_level(cls, v: str):
        if v not in [
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]:
            raise ValueError(
                "Should be one of these value: 'TRACE', 'DEBUG', 'INFO', 'SUCCESS', "
                "'WARNING', 'ERROR', 'CRITICAL'"
            )
        return v

    class Config:
        case_sensitive = True


settings = Settings()
