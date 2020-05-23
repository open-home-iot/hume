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


def new_configuration(uuid, config):
    """
    Interface for handling configuration changes.

    :param uuid: device ID
    :param config: new configuration
    :return:
    """
    LOGGER.info(f"device: {uuid} new configuration: {config}")

    # TODO what to do here? Supply the new configuration to some master planner
    # TODO that when makes sure to schedule actions and set up triggers. What
    # TODO should it be named?
