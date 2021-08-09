from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    PostgresDsn,
    validator,
)


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


client_url_by_env = {
    Environment.DEVELOPMENT: "http://localhost:5000",
    Environment.PRODUCTION: "https://whispers.pyritewolf.dev",
}


class Settings(BaseSettings):
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    CLIENT_URL: Optional[str]

    @validator("CLIENT_URL", pre=True)
    def set_client_url(cls, v: Optional[str], values: Dict[str, Any]):
        return v or client_url_by_env[values["ENVIRONMENT"]]

    JWT_KEY: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]], values: Dict[str, Any]
    ) -> Union[List[str], str]:
        if values.get("ENVIRONMENT") == Environment.DEVELOPMENT:
            return ["http://ui.whispers.lvh.me:5000", "http://localhost:5000"]
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("POSTGRES_HOST"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            path=f"/{values.get('POSTGRES_DB')}",
            port=values.get("POSTGRES_PORT"),
        )

    SQLALCHEMY_TEST_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_TEST_DATABASE_URI", pre=True)
    def assemble_test_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("POSTGRES_HOST"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            path=f"/{values.get('POSTGRES_TEST_DB')}",
            port=values.get("POSTGRES_PORT"),
        )

    DB_POOL_SIZE: int = 20

    # pw recovery
    RESET_PASSWORD_EXPIRATION_SECONDS: int = 86400  # 1 day default
    COOKIE_EXPIRATION_SECONDS: int = 604800  # 7 days default

    # mailing settings
    EMAILS_FROM_NAME: str
    EMAILS_FROM_ADDRESS: str
    MAILGUN_DOMAIN: str
    MAILGUN_KEY: str


class Config:
    case_sensitive = True


settings = Settings()
