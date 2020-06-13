import logging
import os
import sys
import signal
import multiprocessing

from traffic_generator.supervision import hint_req_plugin


def start_hc(monitor_queue: multiprocessing.Queue):
    """
    Starts the hint_controller in a separate thread which can be communicated
    with by HTT.

    :param monitor_queue: reporting queue of the monitor application

    :return: HC supervising process, HC command queue
    """
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()

    hc_proc = ctx.Process(target=hc_loop, args=(q, monitor_queue))
    hc_proc.start()
    print("Started HC supervisor process")

    return hc_proc, q


def set_up_interrupt(mod):
    """
    Ensures that the program can exist gracefully.
    """

    def interrupt(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Interrupted HC: {os.getpid()}")
        mod.test_stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Terminated HC: {os.getpid()}")
        mod.test_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


def hc_loop(q: multiprocessing.Queue, monitor_queue: multiprocessing.Queue):
    """
    Main loop of the hc supervising process.

    :param q: cmd queue of the DC supervisor
    :param monitor_queue: reporting queue of the monitor application
    """
    print(f"hc_loop {os.getpid()}")

    from hume.hint_controller import main as hc_main
    import hint_controller

    # new process, needs termination handlers
    set_up_interrupt(hc_main)

    # Test start method does not block.
    hc_main.test_start(logging.DEBUG)

    # Override the outgoing HINT request module to use HTT's own plugin.
    hint_req_plugin.mq = monitor_queue
    hint_controller.hint.settings

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the HC, for instance: HINT originated requests. For
    # uplink messaging, HTT will receive a call in the hint_req_plugin module
    # when HC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
    while True:
        item = q.get()

        if item == "stop":
            print("HC supervisor stopping")
            break
        else:
            print(f"HC supervisor got: {item}")
