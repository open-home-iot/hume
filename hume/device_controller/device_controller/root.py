import logging
import threading

import hume_storage as storage
from hume_broker import broker

from device_controller.util import args
from device_controller.config import application as config
from device_controller.device import application as device
from device_controller.dispatch import application as dispatch
from device_controller.util import log


LOGGER = logging.getLogger(__name__)

UTIL = [
    broker, storage
]

APPLICATIONS = [
    config, device, dispatch
]


def start(cli_args):
    """
    Starts the RootApp and all its sub-applications.

    :param cli_args: CLI arguments from argparse
    """
    LOGGER.info("root start")

    args.set_args(**vars(cli_args))

    # storage start
    storage.start()  # Must block until started!
    broker.start(log_queue=log.log_queue)

    # model init
    for app in APPLICATIONS:
        app.model_init()

    # pre start
    for app in APPLICATIONS:
        app.pre_start()

    # app start
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

    # This must happen last to track application exits
    log.stop_logging()

    print_exit_status()


def print_exit_status():
    """
    Health check sort of, to see that resources are released properly when
    exiting.
    """
    print("----------------------------------------------")
    print("- STOP RESULTS -")
    print("----------------------------------------------")
    print("# THREADING")
    print(f"# Active threads: {threading.active_count()}")
    print("# List of threads:")
    for thread in threading.enumerate():
        print(f"# {thread}")
