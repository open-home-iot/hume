import multiprocessing
import os
import threading


class MonitorReport:

    def __init__(self):
        pass


def start():
    """
    Starts the monitoring application.

    :return: monitoring app thread, monitored queue
    """
    # needs to be process shared due to HC and DC supervisors being in separate
    # processes
    mq = multiprocessing.Queue()

    t = threading.Thread(target=monitor_loop, args=(mq,))
    t.start()
    print("Started monitor thread")

    return t, mq


def monitor_loop(mq: multiprocessing.Queue):
    """
    Main loop of the monitoring application.
    """
    print(f"monitor_loop {os.getpid()}")

    def get_action(item):
        """
        :param item:
        :return: what command/action was received
        """
        return item

    while True:
        item = mq.get()

        if get_action(item) == "stop":
            print("Monitor app stopping")
            break
        else:
            print(f"monitor got: {item}")

    print("Monitor app broke its loop")
