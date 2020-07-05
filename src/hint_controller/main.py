import signal
import sys
import threading
import argparse
import logging

from hint_controller import root

from hint_controller.util.log import set_up_logging


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME HINT controller"
    )
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
        root.stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        root.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


if __name__ == "__main__":
    args = parse_args()

    set_up_interrupt()

    # Only set up logging if DC is run standalone and not from HTT. Rely on HTT
    # to set up logging otherwise.
    set_up_logging(logging.DEBUG)

    print(f"HC sys.path: {sys.path}")

    root.start(cli_args=args)

    threading.Event().wait()  # Blocks indefinitely
