import logging
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db import session
from app.logger import LOGGER, setup_logger
from app.logo import render


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(LOGGER, logging.INFO),
    after=after_log(LOGGER, logging.DEBUG),
)
def init() -> None:
    try:
        db = session()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        LOGGER.error(e)
        raise e


def main() -> None:
    setup_logger()
    LOGGER.info('\n%s\n', render())
    LOGGER.info("Initialise service...")
    init()
    LOGGER.debug("Service initialisation finished!")


if __name__ == "__main__":
    main()