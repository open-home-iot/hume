import logging
import signal
import sys

from device_controller.util import broker
from device_controller.util.log import set_up_logging

from device_controller.config import application as config
from device_controller.device_listener import application as device_listener
from device_controller.messages import application as messages
from device_controller.rpc import application as rpc


LOGGER = logging.getLogger(__name__)

UTIL = [
    broker
]

APPLICATIONS = [
    config, device_listener, messages, rpc
]


def start(cli_args=None, log_level=None):
    """
    Starts the RootApp and all its sub-applications.

    :param cli_args: CLI arguments from argparse
    :param log_level: log level...
    """
    set_up_logging(log_level)

    LOGGER.info("root start")

    # bind signal handlers
    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)

    # core start
    for app in UTIL:
        app.start()

    # application start
    for app in APPLICATIONS:
        app.start()


def interrupt(_signum, _frame):
    """
    Signal handler for signal.SIGINT

    :param _signum: signal.SIGINT
    :param _frame: N/A
    """
    LOGGER.info("root interrupt")

    stop()
    sys.exit(0)


def terminate(_signum, _frame):
    """
    Signal handler for signal.SIGTERM

    :param _signum: signal.SIGTERM
    :param _frame: N/A
    """
    LOGGER.info("root terminate")

    stop()
    sys.exit(0)


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
