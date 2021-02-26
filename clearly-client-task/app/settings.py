"""settings
"""
from os import getenv
from typing import Any, Optional, Dict

from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Clearly Client"
    PROJECT_DESCRIPTION: str = "Client that connects to the Clearly Server and monitors Tasks"
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = ""
    CLEARLY_SERVER_HOST: str = "clearly-server"
    CLEARLY_SERVER_PORT: str = "12223"
    TASK_SERVICE_HOST: str = "task-service"
    TASK_SERVICE_PORT: str = "8000"
    TASK_SERVICE_API_ENDPOINT: str = "api/v1/tasks/"
    TASK_SERVICE_URI: Optional[AnyHttpUrl] = None

    @validator("TASK_SERVICE_URI", pre=True)
    def assemble_task_service_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AnyHttpUrl.build(
            scheme="http",
            host=values.get("TASK_SERVICE_HOST"),
            port=values.get("TASK_SERVICE_PORT"),
            path=f"/{values.get('TASK_SERVICE_API_ENDPOINT') or ''}",
        )

    class Config:
        case_sensitive = True

settings = Settings()