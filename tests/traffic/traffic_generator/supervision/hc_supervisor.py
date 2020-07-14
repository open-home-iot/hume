import logging
import os
import sys
import signal
import multiprocessing
import traceback

from traffic_generator.simulator import Hint
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


def set_up_interrupt(stop_func):
    """
    Ensures that the program can exist gracefully.
    """

    def interrupt(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Interrupted HC supervisor: {os.getpid()}")
        stop_func()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Terminated HC: {os.getpid()}")
        stop_func()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


def set_up_logging():
    """
    Sets up logging for the DC.
    """
    print(f"HC logging at PID: {os.getpid()}")

    logger = logging.getLogger("hint_controller")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()  # Print logging messages

    formatter = logging.Formatter(fmt="{asctime} {levelname:^8} "
                                      "{module} {message}",
                                  style="{",
                                  datefmt="%d/%m/%Y %H:%M:%S")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)


def hc_loop(q: multiprocessing.Queue, monitor_queue: multiprocessing.Queue):
    """
    Main loop of the hc supervising process.

    :param q: cmd queue of the DC supervisor
    :param monitor_queue: reporting queue of the monitor application
    """
    print(f"hc_loop {os.getpid()}")

    from hint_controller import start, stop, settings
    from hint_controller.hint import hint_req_handler

    # new process, needs termination handlers
    set_up_interrupt(stop)

    # set up DC logging
    set_up_logging()

    # Override the outgoing HINT request module to use HTT's own plugin.
    hint_req_plugin.mq = monitor_queue
    settings._hint_req_mod = hint_req_plugin

    # Start method does not block.
    start()

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the HC, for instance: HINT originated requests. For
    # uplink messaging, HTT will receive a call in the hint_req_plugin module
    # when HC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
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
        print("HC supervisor getting new command")

        try:
            device, operation = q.get()

            operation_tag = get_operation_tag(operation)

            if operation_tag == Hint.CONFIRM_ATTACH:
                hint_req_handler.confirm_attach(device.uuid)

            elif operation_tag == Hint.ACTION:

                # No parent == top device
                if device.parent is None:
                    hint_req_handler.device_action(device.uuid, operation.id)

                else:
                    hint_req_handler.sub_device_action(device.parent.uuid,
                                                       device.id,
                                                       operation.id)

            else:
                print(f"HC supervisor got unrecognized operation tag: "
                      f"{operation_tag} for device: {device}")

        # Bare catch-all causes SIGINT etc. to be caught, derive from Exception
        # to get around that problem. KeyBoardInterrupt derives from
        # BaseException so it will not be caught here.
        except Exception:
            # TODO log caught exceptions with monitor
            traceback.print_exc()
