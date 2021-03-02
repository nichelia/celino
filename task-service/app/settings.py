"""settings
"""
from os import getenv
from typing import Any, Optional, Dict

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Service"
    PROJECT_DESCRIPTION: str = "Task Service API"
    API_ENDPOINT: str = "/api/v1/tasks"
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = ""
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    PROJECT_PREFIX: Optional[str] = None
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("PROJECT_PREFIX", pre=True)
    def assemble_project_prefix(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        project_name = values.get("PROJECT_NAME")
        return "_".join(k.lower() for k in project_name.split())

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True

settings = Settings()