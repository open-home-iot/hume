import logging

from hume_broker import broker
from hume_storage import data_store
from device_controller.util.log import set_up_logging

from device_controller.config import application as config
from device_controller.device import application as device
from device_controller.rpc import application as rpc


LOGGER = logging.getLogger(__name__)

UTIL = [
    broker, data_store
]

APPLICATIONS = [
    config, device, rpc
]


def start(cli_args=None, log_level=logging.INFO):
    """
    Starts the RootApp and all its sub-applications.

    :param cli_args: CLI arguments from argparse
    :param log_level: log level...
    """
    set_up_logging(log_level)

    LOGGER.info("root start")

    # core start
    for app in UTIL:
        app.start()

    # application start
    for app in APPLICATIONS:
        app.start()


def stop():
    """
    Stops all RootApp sub-applications in order to clean up used resources.
    """
    LOGGER.info("root stop")

    # application stop
    for app in APPLICATIONS:
        app.stop()

    # core stop
    for app in UTIL:
        app.stop()
