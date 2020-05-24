import threading
import argparse
import logging

from device_controller import root


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME device controller"
    )
    return parser.parse_args()


def test_start(log_level):
    """
    Used by testing tools to start DC.

    :param log_level:
    """
    root.start(log_level=log_level)


def test_stop():
    """
    Used by test tools to stop DC.
    """
    root.stop()


if __name__ == "__main__":
    args = parse_args()

    root.start(cli_args=args, log_level=logging.DEBUG)

    threading.Event().wait()  # Blocks indefinitely
