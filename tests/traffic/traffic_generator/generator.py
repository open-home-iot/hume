import threading
import time

from traffic_generator.supervision import dc_supervisor, hc_supervisor
from monitoring import monitor
from traffic_generator.device_sim import DeviceSim
from traffic_generator.hint_sim import HintSim

supervision_info = dict()


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

    # Monitor needs to start first to provide its queue to HTT-simulated parts.
    monitor_thread, monitor_queue = monitor.start()
    supervision_info.update({"monitor": (monitor_thread, monitor_queue)})

    # Starts a process which can handle communicating with DC.
    dc_proc, dc_queue = dc_supervisor.start_dc(monitor_queue)
    supervision_info.update({"dc": (dc_proc, dc_queue)})

    # Starts a process which can handle communicating with HC.
    hc_proc, hc_queue = hc_supervisor.start_hc(monitor_queue)
    supervision_info.update({"hc": (hc_proc, hc_queue)})

    # TODO load device specifications
    device_specs = load_device_specs()

    # TODO load HTT configuration
    htt_specs = load_htt_specs()

    # TODO start running traffic based on specs
    run_traffic(device_specs, htt_specs)


def stop():
    """
    Stop HTT.
    """
    dc_proc, dc_queue = supervision_info.get("dc")
    dc_queue.put("stop")  # Necessary? Signals get propagated.
    dc_proc.join()

    hc_proc, hc_queue = supervision_info.get("hc")
    hc_queue.put("stop")  # Necessary? Signals get propagated.
    hc_proc.join()

    monitor_thread, monitor_queue = supervision_info.get("monitor")
    monitor_queue.put("stop")  # Necessary! Signal not propagated to thread.
    monitor_thread.join()


def load_device_specs():
    """
    Load up device specs.
    """
    return {}


def load_htt_specs():
    """
    Load up HTT specs.
    """
    return {}


def run_traffic(device_specs, htt_specs):
    """
    Start traffic.

    :param device_specs:
    :param htt_specs:
    """
    _t, monitor_queue = supervision_info.get("monitor")
    _dc_p, dc_q = supervision_info.get("dc")
    _hc_p, hc_q = supervision_info.get("hc")

    device_sim = DeviceSim(dc_q, monitor_queue)
    hint_sim = HintSim(hc_q, monitor_queue)

    # Some action happens!
    # some_device_params = {"key": "value"}
    # time.sleep(4)
    # device_sim.attach(some_device_params)
    some_hint_params = {"yay": "params"}
    hint_sim.confirm_attach(some_hint_params)

    threading.Event().wait()  # Blocks!
