import threading
import argparse
import logging

from hint_controller import root


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME HINT controller"
    )
    return parser.parse_args()


def test_start(log_level):
    """
    Used by test tools to start HC.

    :param log_level:
    """
    root.start(log_level=log_level)


def test_stop():
    """
    Used by test tools to stop HC.
    """
    root.stop()


if __name__ == "__main__":
    args = parse_args()

    root.start(cli_args=args, log_level=logging.DEBUG)

    threading.Event().wait()  # Blocks indefinitely
