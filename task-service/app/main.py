import socketio
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


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio, static_files={
    "/": "app/app.html",
})
background_task_started = False  


@app.on_event("startup")
async def startup():
    setup_logger()
    LOGGER.debug("API service startup signal received, setting up...")
    await asyncSession.connect()


@app.on_event("shutdown")
async def shutdown():
    LOGGER.debug("API service shutdown signal received, cleaning up...")
    await asyncSession.disconnect()


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        await sio.emit('my_response', {'data': 'Server generated event'})


@sio.on('my_event')
async def test_message(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.on('my_broadcast_event')
async def test_broadcast_message(sid, message):
    await sio.emit('my_response', {'data': message['data']})


@sio.on('join')
async def join(sid, message):
    sio.enter_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
                   room=sid)


@sio.on('leave')
async def leave(sid, message):
    sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                   room=sid)


@sio.on('close room')
async def close(sid, message):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])


@sio.on('my_room_event')
async def send_room_message(sid, message):
    await sio.emit('my_response', {'data': message['data']},
                   room=message['room'])


@sio.on('disconnect request')
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.on('connect')
async def test_connect(sid, environ):
    global background_task_started
    if not background_task_started:
        sio.start_background_task(background_task)
        background_task_started = True
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.on('disconnect')
def test_disconnect(sid):
    print('Client disconnected')


# app.add_middleware(
#     TimingMiddleware,
#     client=ReportTimings(),
#     metric_namer=StarletteScopeToName(prefix=settings.PROJECT_PREFIX, starlette_app=app)
# )
app.include_router(router, prefix=settings.API_ENDPOINT)
app.mount("/", sio_app)