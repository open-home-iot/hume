import functools
import signal
import sys
import threading
import argparse
import logging

import storage
from hume.hume import Hume

from util import set_args, set_up_logger_for, HANDLER_STREAM
from defs import (
    CLI_HUME_UUID,
    CLI_DEVICE_TRANSPORT,
    CLI_DEVICE_TRANSPORT_BLE,
    CLI_DEVICE_TRANSPORT_SIMULATED,
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
    parser.add_argument(CLI_DEVICE_TRANSPORT,
                        metavar="DEVICE_TRANSPORT",
                        choices=(CLI_DEVICE_TRANSPORT_BLE,
                                 CLI_DEVICE_TRANSPORT_SIMULATED),
                        help="Transport medium to use towards devices",
                        nargs="?",
                        default=CLI_DEVICE_TRANSPORT_BLE)

    #
    # Optional arguments
    #

    # Connection args
    parser.add_argument('-hip',
                        '--hint-ip-address',
                        default='127.0.0.1',
                        help="HINT IP address")
    parser.add_argument('-hp',
                        '--hint-port',
                        type=int,
                        default=8000,
                        help="HINT port")

    parser.add_argument('-bip',
                        '--broker-ip-address',
                        default='127.0.0.1',
                        help="Central HINT broker IP address")
    parser.add_argument('-bp',
                        '--broker-port',
                        type=int,
                        default=5672,
                        help="Central HINT broker port")

    # Testing arguments are prepended with "--test", or "-t" for short.

    return parser.parse_args()


def set_up_logging():
    """Sets up DC logging."""
    set_up_logger_for("HUME",
                      None,  # root logger
                      logging.DEBUG,
                      HANDLER_STREAM)
    set_up_logger_for("HUME",
                      "rabbitmq_client",
                      logging.INFO,
                      HANDLER_STREAM)

    # Turn off pika propagation since root logger is in use.
    pika_logger = logging.getLogger("pika")
    pika_logger.propagate = False


def stop(h: Hume):
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


if __name__ == "__main__":
    cli_args = parse_args()
    print(cli_args)

    set_args(**vars(cli_args))
    set_up_logging()

    hume = Hume()

    cb = functools.partial(stop, hume)
    signal.signal(signal.SIGINT, cb)
    signal.signal(signal.SIGTERM, cb)

    hume.start()
