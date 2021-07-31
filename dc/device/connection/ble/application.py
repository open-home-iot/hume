import logging


LOGGER = logging.getLogger(__name__)


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")


def start():
    """
    Starts up the device application.
    """
    LOGGER.info("device start")


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device stop")
