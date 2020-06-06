import logging
import os
import sys
import signal
import multiprocessing

# HUME IMPORTS
sys.path.append(os.path.abspath("../../"))
# For hint controller abs imports to work
sys.path.append(os.path.abspath("../../hume/hint_controller"))

from hume.hint_controller import main as hc_main
from hume.hint_controller.hint_controller.hint import settings
# HUME IMPORTS

from hint_simulator import hint_req_plugin


def start_hc():
    """
    Starts the hint_controller in a separate thread which can be communicated
    with by HTT.
    """
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()

    hc_proc = ctx.Process(target=hc_loop, args=(q,))
    hc_proc.start()
    print("Started HC supervisor process")

    return hc_proc, q


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
        print(f"Interrupted HC: {os.getpid()}")
        hc_main.test_stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Terminated HC: {os.getpid()}")
        hc_main.test_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


def hc_loop(q: multiprocessing.Queue):
    """
    Main loop of the hc supervising process.
    """
    print(f"hc_loop {os.getpid()}")

    # new process, needs termination handlers
    set_up_interrupt()

    # Test start method does not block.
    hc_main.test_start(logging.DEBUG)

    settings.hint_req_mod = hint_req_plugin

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the HC, for instance: HINT originated requests. For
    # uplink messaging, HTT will receive a call in the hint_req_plugin module
    # when HC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
    while True:
        item = q.get()

        if item == "stop":
            break
