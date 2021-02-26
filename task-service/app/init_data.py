from app.db import init_db, session
from app.logger import LOGGER, setup_logger
from app.logo import render


def init() -> None:
    db = session()
    init_db(db)


def main() -> None:
    setup_logger()
    LOGGER.info('\n%s\n', render())
    LOGGER.info("Initialise database...")
    init()
    LOGGER.debug("Database initialisation finished!")


if __name__ == "__main__":
    main()