import signal
import sys
import threading
import argparse
import logging

import hume_storage

from util import args, log
from device import application as device
from dispatch import application as dispatch


LOGGER = logging.getLogger(__name__)

UTIL = [
    hume_storage
]

APPLICATIONS = [
    device, dispatch
]


def start():
    """
    Starts the RootApp and all its sub-applications.
    """
    LOGGER.info("root start")

    # storage start
    hume_storage.start()

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


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME device controller"
    )

    #
    # Positional arguments
    #

    # HUME identification
    parser.add_argument('hume_uuid',
                        metavar="HUME_UUID",
                        help="HUME UUID")

    #
    # Optional arguments
    #

    # Testing arguments are prepended with "--test", or "-t" for short.
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t-dma',
                       '--test-device-mock-address',
                       help="Set up a device mock address where all device "
                            "requests will be routed")
    group.add_argument('-t-rds',
                       '--test-run-device-simulator',
                       help="Run a device simulator, where a single device "
                            "will attach to the HUME on start and can reply "
                            "to all standard requests such as: capability, "
                            "heartbeat, and action",
                       action='store_true')

    # print("Starting DC with the following arguments:")
    # print(parser.parse_args())

    return parser.parse_args()


def set_up_interrupt():
    """
    Ensures that the program can exist gracefully.
    :return:
    """

    def interrupt(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


if __name__ == "__main__":
    cli_args = parse_args()
    args.set_args(**vars(cli_args))

    log.set_up_logging()

    # Only set up logging if DC is run standalone and not from HTT. Rely on HTT
    # to set up logging otherwise.

    # print(f"DC sys.path: {sys.path}")

    set_up_interrupt()
    start()

    threading.Event().wait()  # Blocks indefinitely
