import threading
import argparse
import logging

from device_controller.root import RootApp


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME device controller"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    root_app = RootApp(cli_args=args, log_level=logging.DEBUG)
    root_app.start()

    threading.Event().wait()  # Blocks indefinitely
