import logging
import os
import threading
import queue

import sys

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
    q = queue.Queue()

    hc_thread = threading.Thread(target=hc_loop, args=(q,))
    hc_thread.start()

    return q


def hc_loop(q: queue.Queue):
    """
    Main loop of the hc supervising process.
    """
    # Test start method does not block.
    hc_main.test_start(logging.DEBUG)

    settings.device_req_mod = hint_req_plugin

    # From this point on, HTT can communicate with this supervising process to
    # issue commands to the HC, for instance: HINT originated requests. For
    # uplink messaging, HTT will receive a call in the hint_req_plugin module
    # when HC attempts to send a message to a device. From there, HTT can
    # capture the traffic and update relevant KPIs.
    q.get()
