import logging
import signal
import sys
import os
import multiprocessing

from traffic_generator import start as traffic_start
from traffic_generator import stop as traffic_stop


def set_up_interrupt():
    """
    Ensures that the program can exist gracefully.
    :return:
    """

    def interrupt(_signum, _frame):
        """
        Both DC and HC have been given test stop functions to be able to
        terminate nicely.

        :param _signum:
        :param _frame:
        """
        traffic_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)


if __name__ == "__main__":
    # Set up graceful stop
    set_up_interrupt()

    # Boot the HOME Traffic Tester!
    traffic_start()
