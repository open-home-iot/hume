import logging
import os
import sys
import signal
import multiprocessing

from traffic_generator.supervision import device_req_plugin


def start_dc(monitor_queue: multiprocessing.Queue):
    """
    Starts the device_controller in a separate process which can be communicated
    with by HTT.

    :param monitor_queue: reporting queue of the monitor application

    :return: DC supervising process, DC command queue
    """
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()

    dc_proc = ctx.Process(target=dc_loop, args=(q, monitor_queue))
    dc_proc.start()
    print("Started DC supervisor process")

    return dc_proc, q


def set_up_interrupt(mod):
    """
    Ensures that the program can exist gracefully.
    """

    def interrupt(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Interrupted DC: {os.getpid()}")
        mod.test_stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Terminated DC: {os.getpid()}")
        mod.test_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


def dc_loop(q: multiprocessing.Queue, monitor_queue: multiprocessing.Queue):
    """
    Main loop of the dc supervising process.

    :param q: cmd queue of the DC supervisor
    :param monitor_queue: reporting queue of the monitor application
    """
    print(f"dc_loop {os.getpid()}")

    from hume.device_controller import main as dc_main
    from hume.device_controller.device_controller.device import settings, \
        device_req_handler

    # new process, needs termination handlers
    set_up_interrupt(dc_main)

    # Test start method does not block.
    dc_main.test_start(logging.DEBUG)

    # Override the outgoing device request module to use HTT's own plugin.
    device_req_plugin.mq = monitor_queue
    settings.device_req_mod = device_req_plugin

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the DC, for instance: device originated events. For
    # downlink messaging, HTT will receive a call in the device_req_plugin
    # module when DC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
    while True:
        item = q.get()

        if item == "stop":
            print("DC supervisor stopping")
            break
        else:
            print(f"DC supervisor got: {item}")
            # TODO Do something with the device req handler module of the device
            # controller
