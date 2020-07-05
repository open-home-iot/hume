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

    def get_operation_tag(op):
        """
        :param op:
        :return:
        """
        if isinstance(op, str):
            return op
        else:
            return op.operation_tag

    while True:
        device, operation = mq.get()

        operation_tag = get_operation_tag(operation)

        if operation_tag == "stop":
            print("Monitor app stopping")
            break
        else:
            print(f"Monitor got operation: {operation}")

    print("Monitor app broke its loop")
