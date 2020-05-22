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


if __name__ == "__main__":
    args = parse_args()

    root.start(cli_args=args, log_level=logging.DEBUG)

    threading.Event().wait()  # Blocks indefinitely
