import logging


LOGGER = logging.getLogger(__name__)


def start():
    """
    Starts up the config server.
    """
    LOGGER.info("config start")

    # TODO get config from storage and load it into memory


def stop():
    """
    Not needed for now.
    """
    LOGGER.info("config stop")
