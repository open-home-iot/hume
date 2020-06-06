import logging
import os
import threading
import queue

import sys

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
    q = queue.Queue()

    dc_proc = threading.Thread(target=dc_loop, args=(q,))
    dc_proc.start()

    return q


def dc_loop(q: queue.Queue):
    """
    Main loop of the dc supervising process.
    """
    # Test start method does not block.
    dc_main.test_start(logging.DEBUG)

    settings.device_req_mod = device_req_plugin

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the DC, for instance: device originated events. For
    # downlink messaging, HTT will receive a call in the device_req_plugin
    # module when DC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
    q.get()
