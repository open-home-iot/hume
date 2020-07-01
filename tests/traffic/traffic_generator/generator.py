import datetime
import random
import threading

from monitoring import monitor
from traffic_generator.simulator import Device

from traffic_generator.supervision import dc_supervisor, hc_supervisor
from traffic_generator.simulator.device_sim import DeviceSim
from traffic_generator.specs.spec_parser import load_device_specs, load_htt_specs

supervision_info = dict()
running_timer: threading.Timer

# Randomization part, option for the random engine to choose from.
ORIGIN_DEVICE = "d"
ORIGIN_HINT = "h"
ORIGIN_CHAOS = "c"

ORIGIN_SEQUENCE = [ORIGIN_DEVICE, ORIGIN_HINT]


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

    # Monitor needs to start first to provide its queue to other HTT systems.
    monitor_thread, monitor_queue = monitor.start()
    supervision_info.update({"monitor": (monitor_thread, monitor_queue)})

    # Starts a process which handles DC.
    dc_proc, dc_queue = dc_supervisor.start_dc(monitor_queue)
    supervision_info.update({"dc": (dc_proc, dc_queue)})

    # Starts a process which handles HC.
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
    running_timer.cancel()

    dc_proc, dc_queue = supervision_info.get("dc")
    dc_proc.join()

    hc_proc, hc_queue = supervision_info.get("hc")
    hc_proc.join()

    monitor_thread, monitor_queue = supervision_info.get("monitor")
    monitor_queue.put("stop")  # Necessary! Signal not propagated to thread.
    monitor_thread.join()

    print("All supervised processes and threads have been joined")


def run_traffic(device_specs, htt_specs):
    """
    Start traffic.

    :param device_specs:
    :param htt_specs:
    """
    monitor_t, monitor_q = supervision_info.get("monitor")
    _dc_p, dc_q = supervision_info.get("dc")
    _hc_p, hc_q = supervision_info.get("hc")

    device_sim = DeviceSim(device_specs, dc_q, hc_q, monitor_q)

    print("HTT simulating devices:")
    for device in device_sim.devices:
        print(device)

    # If chaos element should be a part of the traffic scenario
    if htt_specs.chaos_element:
        # Additional random element to pick
        ORIGIN_SEQUENCE.append(ORIGIN_CHAOS)

    # Get number of individual devices
    num_devices = len(device_sim.devices)

    # HTT runs only one timer, how often it times out depends on the number of
    # simulated devices. The more devices, the shorter timer timeout.

    actions_per_minute = htt_specs.actions_per_minute
    # 1 action per minute per device~, depending on settings
    # 1 device = 1 minute timer
    # 5 devices = 60 / 5 = 12
    # or with 2 actions per minute:
    # 5 devices = 60 / 2 / 5 = 6
    # or with 3 actions per minute:
    # 5 devices = 60 / 3 / 5 = 4
    # threading.Timer objects want a float.
    interval = 60.0 / actions_per_minute / num_devices

    print(f"HTT resulting interval: {interval}")

    timer = threading.Timer(
        interval,
        timeout,
        args=(interval, device_sim)
    )

    global running_timer
    running_timer = timer
    print(f"starting timer at: {datetime.datetime.now()}")
    timer.start()

    print("waiting to join monitor...")
    # This is here to prevent a main thread exception when interrupting HTT. If
    # this is not here, the main thread finishes and when the interrupt happens,
    # some exception is raised from the threading module. If the main thread is
    # not allowed to finish, the exception does not occur.
    monitor_t.join()


def timeout(interval, device_sim):
    """
    Traffic generator timeout func.

    :param interval:
    :param device_sim:
    :return:
    """
    print(f"timeout at: {datetime.datetime.now()}")

    origin = random.choice(ORIGIN_SEQUENCE)
    print(f"Random origin: {origin}")
    device: Device = random.choice(device_sim.devices)
    print(f"Chosen device: {device.name}")

    if origin == ORIGIN_DEVICE:
        device_sim.origin_device(device)

    elif origin == ORIGIN_HINT:
        device_sim.origin_hint(device)

    elif origin == ORIGIN_CHAOS:
        device_sim.origin_chaos(device)

    timer = threading.Timer(
        interval,
        timeout,
        args=(interval, device_sim)
    )

    global running_timer
    running_timer = timer

    print(f"starting timer at: {datetime.datetime.now()}")
    timer.start()
