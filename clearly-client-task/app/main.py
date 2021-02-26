import asyncio
import httpx
import json
from clearly.client import ClearlyClient
from clearly.protos.clearly_pb2 import CaptureRequest
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson

from app._version import __version__
from app.logger import LOGGER, setup_logger
from app.logo import render
from app.settings import settings


def post_to_task_service(client, data):
    LOGGER.debug(f"Posting to {settings.TASK_SERVICE_URI} with data {data}")
    r = client.post(settings.TASK_SERVICE_URI, data=data)
    LOGGER.debug(f"Request: {r}")


def parse_task_data(data):
    task_data = MessageToDict(data)
    task_data.pop("timestamp", None)
    task_data.pop("state", None)
    task_data["args"] = []
    task_data["kwargs"] = {}
    return task_data


def init():
    clearly_client = ClearlyClient(
        settings.CLEARLY_SERVER_HOST,
        settings.CLEARLY_SERVER_PORT
    )
    tasks = None
    workers = "!"
    
    tasks_filter = ClearlyClient._parse_pattern(tasks)
    workers_filter = ClearlyClient._parse_pattern(workers)
    request = CaptureRequest(
        tasks_capture=tasks_filter, workers_capture=workers_filter,
    )

    http_client = httpx.Client()

    try:
        for realtime in clearly_client._stub.capture_realtime(request):
            if realtime.HasField('task'):
                if realtime.task.state == "RECEIVED":
                    LOGGER.debug(f"New Task detected with state: {realtime.task.state} and uuid: {realtime.task.uuid}")
                    task_data = parse_task_data(realtime.task)
                    post_to_task_service(http_client, json.dumps(task_data))
    except KeyboardInterrupt:  # pragma: no cover
        pass


def main():
    setup_logger()
    LOGGER.info('\n%s\n', render())
    LOGGER.debug(f"Startup of client...")        
    init()


if __name__ == "__main__":
    main()