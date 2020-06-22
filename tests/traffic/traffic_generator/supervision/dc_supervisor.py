import logging
import os
import sys
import signal
import multiprocessing

from traffic_generator.simulator import DeviceEvent
from traffic_generator.specs.spec_parser import get_device_spec
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


def set_up_interrupt(stop_func):
    """
    Ensures that the program can exist gracefully.
    """

    def interrupt(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Interrupted DC supervisor: {os.getpid()}")
        stop_func()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Terminated DC: {os.getpid()}")
        stop_func()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


def set_up_logging():
    """
    Sets up logging for the DC.
    """
    print(f"DC logging at PID: {os.getpid()}")

    logger = logging.getLogger("device_controller")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()  # Print logging messages

    formatter = logging.Formatter(fmt="{asctime} {levelname:^8} "
                                      "{module} {message}",
                                  style="{",
                                  datefmt="%d/%m/%Y %H:%M:%S")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)


def dc_loop(q: multiprocessing.Queue, monitor_queue: multiprocessing.Queue):
    """
    Main loop of the dc supervising process.

    :param q: cmd queue of the DC supervisor
    :param monitor_queue: reporting queue of the monitor application
    """
    print(f"dc_loop {os.getpid()}")

    from device_controller import start, stop, settings
    from device_controller.device import device_req_handler

    # new process, needs termination handlers
    set_up_interrupt(stop)

    # set up DC logging
    set_up_logging()

    # Test start method does not block.
    start()

    # Override the outgoing device request module to use HTT's own plugin.
    device_req_plugin.mq = monitor_queue
    settings._device_req_mod = device_req_plugin

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the DC, for instance: device originated events. For
    # downlink messaging, HTT will receive a call in the device_req_plugin
    # module when DC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
    while True:
        print("DC supervisor awaiting more commands")
        device, action = q.get()

        print(f"DC supervisor got: {device, action}")

        if action == "attach":
            device_spec = get_device_spec(device)
            device_spec["device_ip"] = f"192.168.0.{device.htt_id}"

            device_req_handler.attach(device_spec)
        elif isinstance(action, DeviceEvent):
            print("DC supervisor got a device event!")
