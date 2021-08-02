import logging


LOGGER = logging.getLogger(__name__)


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")


def start():
    """
    Starts up the ble application.
    """
    LOGGER.info("start")


def stop():
    """
    Stop the ble application.
    """
    LOGGER.info("stop")
