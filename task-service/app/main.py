from fastapi import FastAPI

from app._version import __version__
from app.api import router
from app.db import asyncSession
from app.logger import LOGGER, setup_logger
from app.logo import render
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
    LOGGER.info('\n%s\n', render())
    LOGGER.debug("Startup of webserver...")
    await asyncSession.connect()

@app.on_event("shutdown")
async def shutdown():
    await asyncSession.disconnect()

app.include_router(router, prefix=settings.API_ENDPOINT)
