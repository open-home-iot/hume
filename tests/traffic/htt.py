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

    print(f"HTT PID: {os.getpid()}")

    # IMPORTANT! This should only be done in the main process! Otherwise, the
    # paths get inserted over and over!
    sys.path.insert(0, os.path.abspath("../../hume/device_controller"))
    sys.path.insert(0, os.path.abspath("../../hume/hint_controller"))
    print("printing sys.path")
    print(sys.path)

    # Boot the HOME Traffic Tester!
    traffic_start()
