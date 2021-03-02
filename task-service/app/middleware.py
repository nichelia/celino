from timing_asgi import TimingClient
from app.logger import LOGGER

class ReportTimings(TimingClient):
    def timing(self, metric_name, timing, tags):
        LOGGER.debug(f"Timings Report: {metric_name}, {timing} {tags}")
