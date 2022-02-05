import functools
import signal
import sys
import threading
import argparse
import logging

from hume.app import Hume

from util.log import set_up_logger_for, HANDLER_STREAM
from defs import (
    CLI_HUME_UUID,
)

LOGGER = logging.getLogger(__name__)


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
    parser.add_argument(CLI_HUME_UUID,
                        metavar="HUME_UUID",
                        help="HUME UUID")
    parser.add_argument("--sim",
                        help="Set to simulate devices, deactivates all real "
                             "interfaces",
                        action='store_true')

    #
    # Optional arguments
    #

    # Connection args
    parser.add_argument("-hip",
                        "--hint-ip-address",
                        default="127.0.0.1",
                        help="HINT IP address")
    parser.add_argument("-hp",
                        "--hint-port",
                        type=int,
                        default=8000,
                        help="HINT port")

    parser.add_argument("-bip",
                        "--broker-ip-address",
                        default="127.0.0.1",
                        help="Central HINT broker IP address")
    parser.add_argument("-bp",
                        "--broker-port",
                        type=int,
                        default=5672,
                        help="Central HINT broker port")

    # PSQL args
    parser.add_argument("-pu",
                        "--psql-user",
                        default="hume",
                        help="PSQL username")
    parser.add_argument("-pu",
                        "--psql-user",
                        default="password",
                        help="PSQL password")

    # Testing arguments are prepended with "--test", or "-t" for short.

    return parser.parse_args()


def set_up_logging():
    """Sets up DC logging."""
    set_up_logger_for(None,  # root logger
                      logging.DEBUG,
                      HANDLER_STREAM)
    set_up_logger_for("rabbitmq_client",
                      logging.INFO,
                      HANDLER_STREAM)

    # Turn off pika propagation since root logger is in use.
    pika_logger = logging.getLogger("pika")
    pika_logger.propagate = False


def stop(h: Hume, _a, _b):
    """Stop everything!"""

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

    h.stop()
    print_exit_status()
    sys.exit(0)


if __name__ == "__main__":
    set_up_logging()

    cli_args = parse_args()
    print(cli_args)
    hume = Hume(vars(cli_args))

    cb = functools.partial(stop, hume)
    signal.signal(signal.SIGINT, cb)
    signal.signal(signal.SIGTERM, cb)

    hume.start()
    threading.Event().wait()
