import functools
import signal
import sys
import threading
import argparse
import logging

from hume.app import Hume

from util.log import set_up_logger_for, HANDLER_STREAM
from defs import CLI_HUME_UUID, CLI_DEBUG

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
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

    #
    # Optional arguments
    #

    # HINT connection args
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

    # Logging
    parser.add_argument("-d",
                        "--debug",
                        help="Enable debug logging",
                        action='store_true')

    # Device simulation
    parser.add_argument("--sim",
                        help="Set to simulate devices, deactivates all real "
                             "interfaces",
                        action='store_true')

    # Testing arguments are prepended with "--test", or "-t" for short.

    return parser.parse_args()


def set_up_logging(_cli_args: dict):
    """Sets up HUME logging."""
    set_up_logger_for(None,  # root logger
                      logging.DEBUG if _cli_args[CLI_DEBUG]
                      else logging.INFO,
                      HANDLER_STREAM)
    set_up_logger_for("rabbitmq_client",
                      logging.DEBUG if _cli_args[CLI_DEBUG]
                      else logging.WARNING,
                      HANDLER_STREAM)
    set_up_logger_for("pika",
                      logging.DEBUG if _cli_args[CLI_DEBUG]
                      else logging.WARNING,
                      HANDLER_STREAM)


def stop(h: Hume, _a, _b):
    """
    Stop everything!
    """
    exit_code = 0
    try:
        h.stop()
    except Exception as exc:
        exit_code = 1  # something went wrong!
        LOGGER.info(f"exception {exc} happened when shutting down")

    log_exit_status()
    sys.exit(exit_code)


def log_exit_status():
    """
    Health check sort of, to see that resources are released properly when
    exiting.
    """
    exit_status = f"""exit status:

    ----------------------------------------------
                  HUME EXIT STATUS
    ----------------------------------------------
                    - THREADS -
    ----------------------------------------------
    Active threads:  {threading.active_count()}
    List of threads: {threading.enumerate()}
    """

    LOGGER.info(exit_status)


if __name__ == "__main__":
    cli_args = parse_args()
    print(cli_args)
    set_up_logging(vars(cli_args))

    hume = Hume(vars(cli_args))

    cb = functools.partial(stop, hume)
    signal.signal(signal.SIGINT, cb)
    signal.signal(signal.SIGTERM, cb)

    try:
        hume.start()
        threading.Event().wait()
    except Exception as e:
        LOGGER.info(f"exception {e} happened when starting")
        # no need to call hume stop for cleanup, hume will cleanly stop when
        # failing to start, or at least it should.
        log_exit_status()
        sys.exit(1)  # something went wrong!
