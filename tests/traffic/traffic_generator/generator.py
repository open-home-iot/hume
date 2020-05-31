import threading

from traffic_generator import dc_supervisor
from traffic_generator import hc_supervisor


def start():
    """
    Starting point for the traffic generator/tester.

    :return:
    """
    # Applications have to be run in isolation, or they will collide as they're
    # using similar, if not the same, module imports. A typical clash is the
    # hume_broker and its reference to a rabbitMQ client.
    #
    # The traffic tester needs to call functions in both applications, example
    # flow:
    # 1. HTT invokes a device originated message by calling a DEVICE
    #    EVENT >> function << in the DC.
    # 2. DC handles the event and forwards it to the HC over RMQ.
    # 3. HC receives the message over RMQ and sends HINT a DEVICE EVENT message,
    #    where HINT is a HTT mocked module for tracking traffic KPIs.
    #
    # This means that HTT needs access to both process spaces to be able to
    # invoke messages originated either from a device or HINT.

    # Starts a process which can handle communicating with DC.
    dc_supervisor.start_dc()

    # Starts a process which can handle communicating with HC.
    hc_supervisor.start_hc()

    # TODO load device specifications
    load_device_specs()
    # TODO start running traffic based on specs
    run_traffic()


def stop():
    print("yay")


def load_device_specs():
    pass


def run_traffic():
    pass
