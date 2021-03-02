from fastapi import FastAPI
from timing_asgi import TimingMiddleware
from timing_asgi.integrations import StarletteScopeToName

from app._version import __version__
from app.api import router
from app.db import asyncSession
from app.logger import LOGGER, setup_logger
from app.logo import render
from app.middleware import ReportTimings
from app.settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    openapi_url=f"{settings.API_ENDPOINT}/openapi.json",
    version=__version__,
)


@app.on_event("startup")
async def startup():
    setup_logger()
    LOGGER.debug("API service startup signal received, setting up...")
    await asyncSession.connect()


@app.on_event("shutdown")
async def shutdown():
    LOGGER.debug("API service shutdown signal received, cleaning up...")
    await asyncSession.disconnect()


app.add_middleware(
    TimingMiddleware,
    client=ReportTimings(),
    metric_namer=StarletteScopeToName(prefix=settings.PROJECT_PREFIX, starlette_app=app)
)
app.include_router(router, prefix=settings.API_ENDPOINT)
