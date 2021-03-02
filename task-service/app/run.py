import uvicorn
from app.logger import LOGGER, setup_logger
from app.logo import render


def init() -> None:
    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True, debug=True)


def main() -> None:
    setup_logger()
    LOGGER.info('\n%s\n', render())
    LOGGER.info("Run webserver...")
    init()
    LOGGER.debug("Webserver running finished!")


if __name__ == "__main__":
    main()