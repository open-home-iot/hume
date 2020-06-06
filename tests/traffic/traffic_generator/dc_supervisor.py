import logging
import os
import sys
import signal
import multiprocessing

# HUME IMPORTS
sys.path.append(os.path.abspath("../../"))
# For device controller abs imports to work
sys.path.append(os.path.abspath("../../hume/device_controller"))

from hume.device_controller import main as dc_main
from hume.device_controller.device_controller.device import settings
# HUME IMPORTS

from device_simulator import device_req_plugin


def start_dc():
    """
    Starts the device_controller in a separate process which can be communicated
    with by HTT.
    """
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()

    dc_proc = ctx.Process(target=dc_loop, args=(q,))
    dc_proc.start()
    print("Started DC supervisor process")

    return dc_proc, q


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
        print(f"Interrupted DC: {os.getpid()}")
        dc_main.test_stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Terminated DC: {os.getpid()}")
        dc_main.test_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


def dc_loop(q: multiprocessing.Queue):
    """
    Main loop of the dc supervising process.
    """
    print(f"dc_loop {os.getpid()}")

    # new process, needs termination handlers
    set_up_interrupt()

    # Test start method does not block.
    dc_main.test_start(logging.DEBUG)

    settings.device_req_mod = device_req_plugin

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the DC, for instance: device originated events. For
    # downlink messaging, HTT will receive a call in the device_req_plugin
    # module when DC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
    while True:
        item = q.get()

        if item == "stop":
            break
