import logging
import signal
import threading

import sys
import os


sys.path.append(os.path.abspath("../.."))
# For device controller abs imports to work
sys.path.append(os.path.abspath("../../hume/device_controller"))
# For hint controller abs imports to work
sys.path.append(os.path.abspath("../../hume/hint_controller"))

from hume.device_controller import main as dc_main
from hume.hint_controller import main as hc_main


dc_main.test_start(logging.DEBUG)
hc_main.test_start(logging.DEBUG)


def set_up_interrupt():
    def interrupt(_signum, _frame):
        dc_main.test_stop()
        hc_main.test_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)


set_up_interrupt()

threading.Event().wait()  # Blocks!
