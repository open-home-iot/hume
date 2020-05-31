import logging
import multiprocessing
import os
import threading

import sys

# HUME IMPORTS
sys.path.append(os.path.abspath("../.."))
# For device controller abs imports to work
sys.path.append(os.path.abspath("../../../hume/hint_controller"))

from hume.hint_controller import main as hc_main
from hume.hint_controller.hint_controller.hint import settings
# HUME IMPORTS

from hint_simulator import hint_req_plugin


def start_hc():
    """
    Starts the hint_controller in a separate process which can be communicated
    with by HTT.
    """
    hc_proc = multiprocessing.Process(target=hc_loop)
    hc_proc.start()


def hc_loop():
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
    threading.Event().wait()
