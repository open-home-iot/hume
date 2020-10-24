import logging

from hume_broker import broker
from hume_storage import data_store

from hint_controller.util import args

from hint_controller.rpc import application as rpc
from hint_controller.hint import application as hint


LOGGER = logging.getLogger(__name__)

UTIL = [
    broker, data_store
]

APPLICATIONS = [
    rpc, hint
]


def start(cli_args):
    """
    Starts the RootApp and all its sub-applications.

    :param cli_args: CLI arguments
    """
    LOGGER.info("root start")

    args.set_args(**vars(cli_args))

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
