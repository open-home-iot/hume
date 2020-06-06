import os
import signal
import sys

from traffic_generator import start as traffic_start
from traffic_generator import stop as traffic_stop


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
        print(f"Interrupted HTT: {os.getpid()}")
        traffic_stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Terminated HTT: {os.getpid()}")
        traffic_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


if __name__ == "__main__":
    # Set up graceful stop
    set_up_interrupt()

    print(f"HTT started: {os.getpid()}")

    # Boot the HOME Traffic Tester!
    traffic_start()
