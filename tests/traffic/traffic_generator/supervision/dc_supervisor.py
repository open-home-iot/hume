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


def set_up_interrupt(stop_func):
    """
    Ensures that the program can exist gracefully.
    """

    def interrupt(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        print(f"Interrupted DC: {os.getpid()}")
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
    def get_action(item):
        """
        :param item:
        :return: what command/action was received
        """
        return item

    while True:
        item = q.get()

        if get_action(item) == "stop":
            print("DC supervisor stopping")
            break
        else:
            print(f"DC supervisor got: {item}")

            device_req_handler.attach(
                {
                    "name": "Greenhouse",
                    "uuid": "0a4636be-40e1-460c-8b12-6d93108e3dc7",
                    "device_ip": "192.168.0.1",
                    "class": "COMPOUND",
                    "spec": "GREENHOUSE",
                    "devices": [
                        {
                            "name": "Thermometer",
                            "id": 3,
                            "class": "SENSOR",
                            "spec": "THERMOMETER",
                            "actions": [
                                {
                                    "name": "Temperature",
                                    "id": 1,
                                    "type": "READ",
                                    "return_type": "FLOAT"
                                }
                            ]
                        },
                        {
                            "name": "Water Level Sensor",
                            "id": 4,
                            "class": "SENSOR",
                            "spec": "WATER_LEVEL",
                            "actions": [
                                {
                                    "name": "Water Level",
                                    "id": 1,
                                    "type": "READ",
                                    "return_type": "PERC_INT"
                                }
                            ],
                            "events": [
                                {
                                    "info": "Water Level Warning",
                                    "id": 1,
                                    "data_type": "PERC_INT"
                                },
                                {
                                    "info": "Water Level High",
                                    "id": 2
                                }
                            ]
                        }
                    ]
                }
            )

    print("DC supervisor broke its loop")
